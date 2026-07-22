from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
import json, uuid
import discord
from discord.ext import commands, tasks

# --- データモデル ---

@dataclass
class Reminder:
    id: str
    due_at: datetime           # 期日
    body: str                  # 本文
    user_id: str               # 予約したユーザー
    channel_id: str            # 返信先チャネル

STORAGE = Path("reminders.json")

# --- 永続化 (失敗しうる) ---

def load_reminders() -> dict[str, Reminder]:
    if not STORAGE.exists():
        return {}
    try:
        raw = json.loads(STORAGE.read_text())
    except (OSError, json.JSONDecodeError) as e:
        raise RuntimeError(f"読み込み失敗: {e}")
    return {
        r["id"]: Reminder(
            id=r["id"],
            due_at=datetime.fromisoformat(r["due_at"]),
            body=r["body"],
            user_id=r["user_id"],
            channel_id=r["channel_id"],
        )
        for r in raw
    }

def save_reminders(reminders: dict[str, Reminder]) -> None:
    try:
        payload = [
            {**asdict(r), "due_at": r.due_at.isoformat()}
            for r in reminders.values()
        ]
        STORAGE.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    except OSError as e:
        raise RuntimeError(f"書き込み失敗: {e}")

# --- 時刻パース (失敗しうる) ---

def parse_time(text: str) -> datetime:
    # 想定入力: "2026-07-05 09:00"
    try:
        return datetime.fromisoformat(text.replace(" ", "T"))
    except ValueError:
        raise ValueError(f"時刻フォーマット不正: {text}")

# --- コマンド分岐 (dispatcher) ---

async def handle_remind(ctx, args: str, reminders: dict[str, Reminder]):
    parts = args.split(None, 2)
    if not parts:
        await ctx.send("使い方: !remind YYYY-MM-DD HH:MM 本文 | list | cancel <id>")
        return

    match parts[0]:
        case "list":
            if not reminders:
                await ctx.send("予約はありません")
                return
            lines = [
                f"{r.id}: {r.due_at.isoformat()} {r.body}"
                for r in reminders.values()
            ]
            await ctx.send("\n".join(lines))

        case "cancel":
            if len(parts) < 2:
                await ctx.send("id を指定してください")
                return
            target_id = parts[1]
            if target_id not in reminders:
                await ctx.send(f"予約 {target_id} が見つかりません")
                return
            del reminders[target_id]
            try:
                save_reminders(reminders)
            except RuntimeError as e:
                await ctx.send(f"保存失敗: {e}")
                return
            await ctx.send(f"予約 {target_id} をキャンセルしました")

        case _:
            # !remind <YYYY-MM-DD> <HH:MM> <本文>
            if len(parts) < 3:
                await ctx.send("引数不足: !remind YYYY-MM-DD HH:MM 本文")
                return
            time_str = f"{parts[0]} {parts[1]}"
            body = parts[2]
            try:
                due = parse_time(time_str)
            except ValueError as e:
                await ctx.send(str(e))
                return

            rid = str(uuid.uuid4())[:8]
            new_r = Reminder(
                id=rid,
                due_at=due,
                body=body,
                user_id=str(ctx.author.id),
                channel_id=str(ctx.channel.id),
            )
            reminders[rid] = new_r
            try:
                save_reminders(reminders)
            except RuntimeError as e:
                # 保存失敗したのでインメモリもロールバック
                del reminders[rid]
                await ctx.send(f"保存失敗、予約を取り消しました: {e}")
                return
            await ctx.send(f"予約しました (id: {rid})")

# --- 背景タスク: 期日到来検出 + 通知 ---

async def check_due(bot, reminders: dict[str, Reminder]):
    now = datetime.now()
    due_ids = [
        rid for rid, r in reminders.items()
        if r.due_at <= now
    ]
    for rid in due_ids:
        r = reminders.pop(rid)
        channel = bot.get_channel(int(r.channel_id))
        if channel:
            await channel.send(f"<@{r.user_id}> リマインダー: {r.body}")
    if due_ids:
        try:
            save_reminders(reminders)
        except RuntimeError as e:
            # 通知は成功しているので次回リトライで良い
            print(f"通知後書き込み失敗 (無視): {e}")

# --- Bot エントリポイント ---

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
reminders: dict[str, Reminder] = {}

@bot.event
async def on_ready():
    global reminders
    try:
        reminders = load_reminders()
    except RuntimeError as e:
        print(f"起動時読み込み失敗、空で開始: {e}")
    check_due_loop.start()

@bot.command(name="remind")
async def cmd_remind(ctx, *, args: str = ""):
    await handle_remind(ctx, args, reminders)

@tasks.loop(seconds=30)
async def check_due_loop():
    await check_due(bot, reminders)

bot.run("TOKEN")