"""
Interactive Terminal Interface for ChatRecall
=============================================
Provides interactive and command-line search with rich formatting, query plan inspection,
thread context expansion, and comparison against standard keyword search.
"""

import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from src.index import ChatIndex
from src.retrieve import RetrievalEngine
from src.context import ThreadContextBuilder


console = Console()


def display_results(search_res: dict, context_builder: ThreadContextBuilder, show_threads: bool = True):
    query = search_res["query"]
    plan = search_res["plan"]
    results = search_res["results"]

    # Header Panel
    plan_info = f"[bold cyan]Strategy:[/bold cyan] {plan['strategy'].upper()}"
    if plan["target_person"]:
        plan_info += f"  |  [bold yellow]Person:[/bold yellow] {plan['target_person']}"
    if plan["time_range"]:
        plan_info += f"  |  [bold green]Time Window:[/bold green] {plan['time_range'][0]} to {plan['time_range'][1]}"
    if plan["is_decision_query"]:
        plan_info += f"  |  [bold magenta]Intent:[/bold magenta] 🎯 Decision Resolution"

    console.print(Panel(
        f"[bold white]Query:[/bold white] \"{query}\"\n{plan_info}\n[dim]Candidates evaluated: {search_res['candidate_count']}[/dim]",
        title="🔍 [bold]ChatRecall Search[/bold]",
        border_style="cyan"
    ))

    if not results:
        console.print("[bold red]No matching messages found.[/bold red]")
        return

    for item in results:
        rank = item["rank"]
        sender = item["sender"]
        ts = item["timestamp"]
        text = item["message"]
        score = item["score"]
        is_dec = item["is_decision"]
        msg_id = item["id"]
        msg_idx = item["msg_idx"]

        badge = " 🏆 [bold green][DECISION RESOLUTION][/bold green]" if is_dec else ""
        title = f"Match #{rank} (ID: {msg_id}) • Score: {score:.4f}{badge}"

        if show_threads:
            ctx = context_builder.get_context_window(msg_idx, window_before=2, window_after=2)
            table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold magenta", expand=True)
            table.add_column("Time", style="dim", width=22)
            table.add_column("Sender", style="cyan", width=18)
            table.add_column("Message", style="white")

            for cm in ctx["messages"]:
                c_time = cm["formatted_time"]
                c_sender = cm["sender"]
                c_text = cm["message"]
                if cm["is_target"]:
                    c_sender = f"[bold yellow]👉 {c_sender}[/bold yellow]"
                    c_text = f"[bold green on grey15]{c_text}[/bold green on grey15]"
                elif cm["is_decision"]:
                    c_text = f"[italic green]{c_text}[/italic green]"

                table.add_row(c_time, c_sender, c_text)

            console.print(Panel(table, title=title, border_style="green" if rank == 1 else "blue"))
        else:
            console.print(Panel(
                f"[bold cyan]{sender}[/bold cyan] [dim]({ts})[/dim]:\n{text}",
                title=title,
                border_style="green" if rank == 1 else "blue"
            ))


def main():
    parser = argparse.ArgumentParser(description="ChatRecall Semantic Search CLI")
    parser.add_argument("--query", "-q", type=str, help="Search query")
    parser.add_argument("--top_k", "-k", type=int, default=3, help="Number of top results to return")
    parser.add_argument("--no_thread", action="store_true", help="Disable thread context view")
    args = parser.parse_args()

    console.print("[dim]Loading index and embedder...[/dim]")
    index = ChatIndex.build_or_load()
    engine = RetrievalEngine(index)
    ctx_builder = ThreadContextBuilder(index)

    if args.query:
        res = engine.search(args.query, top_k=args.top_k)
        display_results(res, ctx_builder, show_threads=not args.no_thread)
    else:
        console.print("[bold green]ChatRecall Interactive Terminal[/bold green] (type 'exit' to quit)\n")
        while True:
            try:
                q = console.input("[bold yellow]Enter Search Query > [/bold yellow]").strip()
                if not q or q.lower() in ["exit", "quit", "q"]:
                    break
                res = engine.search(q, top_k=args.top_k)
                display_results(res, ctx_builder, show_threads=not args.no_thread)
                console.print("\n" + "─" * 60 + "\n")
            except (KeyboardInterrupt, EOFError):
                break


if __name__ == "__main__":
    main()
