"""
Evaluation Runner for sample_chat.txt and questions.json
=========================================================
Runs the 20-question evaluation benchmark on sample_chat.txt.
Reports:
  1. Top-1, Top-3, Top-5 Accuracy and MRR across all 20 questions
  2. Hard (zero-word-overlap) Top-1, Top-3, Top-5 Accuracy and MRR (questions q16-q20)
  3. Warm-up / standard queries breakdown (semantic, person, time)
  4. Per-query detailed results with retrieved rank, score, and message snippet
"""

import json
import os
import sys
import time
from typing import List, Dict, Any

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath("."))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.index import ChatIndex
from src.retrieve import RetrievalEngine

console = Console()


def compute_metrics(records: List[Dict[str, Any]]) -> Dict[str, float]:
    total = len(records)
    if total == 0:
        return {"count": 0, "top_1_acc": 0.0, "top_3_acc": 0.0, "top_5_acc": 0.0, "mrr": 0.0}

    top_1 = sum(1 for r in records if r.get("rank") == 1)
    top_3 = sum(1 for r in records if r.get("rank") is not None and 1 <= r["rank"] <= 3)
    top_5 = sum(1 for r in records if r.get("rank") is not None and 1 <= r["rank"] <= 5)
    mrr = sum(1.0 / r["rank"] for r in records if r.get("rank") is not None) / total

    return {
        "count": total,
        "top_1": top_1,
        "top_3": top_3,
        "top_5": top_5,
        "top_1_acc": round(top_1 / total * 100, 2),
        "top_3_acc": round(top_3 / total * 100, 2),
        "top_5_acc": round(top_5 / total * 100, 2),
        "mrr": round(mrr, 4),
    }


def run_demo_benchmark(
    chat_file: str = "sample_chat.txt",
    questions_file: str = "questions.json",
    verbose: bool = True
) -> Dict[str, Any]:
    console.print(Panel.fit(
        f"[bold cyan]ChatRecall Demo Benchmark[/bold cyan]\n"
        f"Chat: [green]{chat_file}[/green] | Questions: [green]{questions_file}[/green]",
        border_style="cyan"
    ))

    # Load questions
    with open(questions_file, "r", encoding="utf-8") as f:
        questions = json.load(f)

    # Build / load index
    index = ChatIndex.build_or_load(chat_file, force_rebuild=False)
    engine = RetrievalEngine(index)

    records = []
    start_time = time.time()

    for q in questions:
        qid = q["id"]
        query = q["query"]
        target_int = q["answer_id"]
        target_str = f"MSG_{target_int:05d}"
        q_type = q.get("type", "semantic")
        is_hard = "hard" in q_type
        note = q.get("note", "")

        # Search top 10
        search_res = engine.search(query, top_k=10)
        results = search_res["results"]

        matched_rank = None
        matched_score = None
        for r in results:
            m_id = r["id"]
            if m_id == target_int or m_id == target_str or m_id == str(target_int):
                matched_rank = r["rank"]
                matched_score = r["score"]
                break

        top1 = results[0] if results else None
        records.append({
            "id": qid,
            "query": query,
            "target_id": target_int,
            "type": q_type,
            "is_hard": is_hard,
            "note": note,
            "rank": matched_rank,
            "score": matched_score,
            "strategy": search_res["plan"]["strategy"],
            "top1_id": top1["id"] if top1 else None,
            "top1_sender": top1["sender"] if top1 else None,
            "top1_text": top1["message"] if top1 else None,
            "top1_score": top1["score"] if top1 else None,
        })

    elapsed = time.time() - start_time

    # Compute metric breakdowns
    all_metrics = compute_metrics(records)
    hard_records = [r for r in records if r["is_hard"]]
    hard_metrics = compute_metrics(hard_records)
    warmup_records = [r for r in records if not r["is_hard"]]
    warmup_metrics = compute_metrics(warmup_records)

    # Types breakdown
    types = sorted(list(set(r["type"] for r in records)))
    type_metrics = {}
    for t in types:
        t_recs = [r for r in records if r["type"] == t]
        type_metrics[t] = compute_metrics(t_recs)

    if verbose:
        # Detailed Per-Query Table
        table = Table(title="📋 Per-Query Detailed Retrieval Results", show_lines=True)
        table.add_column("QID", style="bold", width=6)
        table.add_column("Type", width=14)
        table.add_column("Query", width=38)
        table.add_column("Target ID", justify="center", width=10)
        table.add_column("Rank", justify="center", width=8)
        table.add_column("Score", justify="right", width=8)
        table.add_column("Top-1 Retrieved Message", width=42)

        for r in records:
            rank_str = f"[bold green]Rank 1[/bold green]" if r["rank"] == 1 else (
                f"[yellow]Rank {r['rank']}[/yellow]" if r["rank"] and r["rank"] <= 3 else (
                    f"[red]Rank {r['rank']}[/red]" if r["rank"] else "[bold red]MISS[/bold red]"
                )
            )
            score_str = f"{r['score']:.4f}" if r["score"] is not None else "-"
            top1_str = f"{r['top1_sender']}: {r['top1_text'][:40]}..." if r["top1_text"] else "-"

            table.add_row(
                r["id"],
                f"[magenta]{r['type']}[/magenta]",
                r["query"],
                str(r["target_id"]),
                rank_str,
                score_str,
                top1_str
            )

        console.print(table)

        # Summary Metrics Table
        summary_table = Table(title="🎯 Benchmark Summary Metrics", show_lines=True)
        summary_table.add_column("Query Subset", style="bold cyan", width=24)
        summary_table.add_column("Count", justify="center", width=8)
        summary_table.add_column("Top-1 Acc", justify="right", width=12)
        summary_table.add_column("Top-3 Acc", justify="right", width=12)
        summary_table.add_column("Top-5 Acc", justify="right", width=12)
        summary_table.add_column("MRR", justify="right", width=10)

        summary_table.add_row(
            "[bold]All Questions (Total)[/bold]",
            str(all_metrics["count"]),
            f"{all_metrics['top_1_acc']}% ({all_metrics['top_1']}/{all_metrics['count']})",
            f"{all_metrics['top_3_acc']}% ({all_metrics['top_3']}/{all_metrics['count']})",
            f"{all_metrics['top_5_acc']}% ({all_metrics['top_5']}/{all_metrics['count']})",
            f"{all_metrics['mrr']:.4f}"
        )
        summary_table.add_row(
            "[bold yellow]Hard (Zero-Overlap)[/bold yellow]",
            str(hard_metrics["count"]),
            f"{hard_metrics['top_1_acc']}% ({hard_metrics['top_1']}/{hard_metrics['count']})",
            f"{hard_metrics['top_3_acc']}% ({hard_metrics['top_3']}/{hard_metrics['count']})",
            f"{hard_metrics['top_5_acc']}% ({hard_metrics['top_5']}/{hard_metrics['count']})",
            f"{hard_metrics['mrr']:.4f}"
        )
        summary_table.add_row(
            "Warmup / Standard",
            str(warmup_metrics["count"]),
            f"{warmup_metrics['top_1_acc']}% ({warmup_metrics['top_1']}/{warmup_metrics['count']})",
            f"{warmup_metrics['top_3_acc']}% ({warmup_metrics['top_3']}/{warmup_metrics['count']})",
            f"{warmup_metrics['top_5_acc']}% ({warmup_metrics['top_5']}/{warmup_metrics['count']})",
            f"{warmup_metrics['mrr']:.4f}"
        )

        for t, tm in type_metrics.items():
            summary_table.add_row(
                f"  └ Type: {t}",
                str(tm["count"]),
                f"{tm['top_1_acc']}%",
                f"{tm['top_3_acc']}%",
                f"{tm['top_5_acc']}%",
                f"{tm['mrr']:.4f}"
            )

        console.print(summary_table)
        console.print(f"[dim]Benchmark completed in {elapsed:.2f}s[/dim]\n")

    return {
        "all": all_metrics,
        "hard": hard_metrics,
        "warmup": warmup_metrics,
        "by_type": type_metrics,
        "records": records,
        "elapsed_sec": round(elapsed, 2)
    }


if __name__ == "__main__":
    run_demo_benchmark()
