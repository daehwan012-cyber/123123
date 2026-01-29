"""
로또(6/45) 번호 추천기 - CLI

예)
  python lotto.py
  python lotto.py -n 5
  python lotto.py -n 3 --exclude 7,13,25 --fixed 1,2
"""

from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class LottoConfig:
    games: int = 5
    min_number: int = 1
    max_number: int = 45
    pick: int = 6
    fixed: tuple[int, ...] = ()
    exclude: tuple[int, ...] = ()


def _parse_csv_ints(raw: str) -> list[int]:
    if raw is None:
        return []
    s = raw.strip()
    if not s:
        return []
    parts = [p.strip() for p in s.split(",")]
    out: list[int] = []
    for p in parts:
        if not p:
            continue
        try:
            out.append(int(p))
        except ValueError as e:
            raise argparse.ArgumentTypeError(f"숫자가 아닙니다: {p!r}") from e
    return out


def _validate_numbers(
    *,
    values: Iterable[int],
    min_number: int,
    max_number: int,
    label: str,
) -> tuple[int, ...]:
    vals = list(values)
    for v in vals:
        if v < min_number or v > max_number:
            raise ValueError(f"{label} 범위 오류: {v} (허용: {min_number}~{max_number})")
    # 입력 순서와 무관하게 중복 제거
    return tuple(sorted(set(vals)))


def generate_games(cfg: LottoConfig, rng: random.Random | None = None) -> list[tuple[int, ...]]:
    if rng is None:
        rng = random.SystemRandom()

    if cfg.games < 1:
        raise ValueError("게임 수는 1 이상이어야 합니다.")
    if cfg.pick < 1:
        raise ValueError("뽑을 개수는 1 이상이어야 합니다.")
    if cfg.min_number >= cfg.max_number:
        raise ValueError("최소값은 최대값보다 작아야 합니다.")

    fixed = _validate_numbers(
        values=cfg.fixed, min_number=cfg.min_number, max_number=cfg.max_number, label="고정번호"
    )
    exclude = _validate_numbers(
        values=cfg.exclude, min_number=cfg.min_number, max_number=cfg.max_number, label="제외번호"
    )

    fixed_set = set(fixed)
    exclude_set = set(exclude)
    conflict = fixed_set & exclude_set
    if conflict:
        raise ValueError(f"고정번호와 제외번호가 겹칩니다: {sorted(conflict)}")
    if len(fixed) > cfg.pick:
        raise ValueError(f"고정번호 개수({len(fixed)})가 뽑을 개수({cfg.pick})보다 많습니다.")

    pool = [n for n in range(cfg.min_number, cfg.max_number + 1) if n not in exclude_set and n not in fixed_set]
    need = cfg.pick - len(fixed)
    if len(pool) < need:
        raise ValueError(
            f"가능한 숫자가 부족합니다. (필요 {need}개, 가능 {len(pool)}개) 제외/고정 번호를 줄여주세요."
        )

    games: list[tuple[int, ...]] = []
    for _ in range(cfg.games):
        picks = list(fixed) + rng.sample(pool, k=need)
        picks.sort()
        games.append(tuple(picks))
    return games


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="로또(6/45) 번호 추천기")
    p.add_argument("-n", "--games", type=int, default=5, help="생성할 게임 수 (기본: 5)")
    p.add_argument("--exclude", type=str, default="", help="제외할 번호 CSV (예: 7,13,25)")
    p.add_argument("--fixed", type=str, default="", help="반드시 포함할 번호 CSV (예: 1,2)")
    return p


def main(argv: list[str]) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        cfg = LottoConfig(
            games=args.games,
            fixed=tuple(_parse_csv_ints(args.fixed)),
            exclude=tuple(_parse_csv_ints(args.exclude)),
        )
        games = generate_games(cfg)
    except Exception as e:
        print(f"[오류] {e}", file=sys.stderr)
        return 2

    for i, g in enumerate(games, start=1):
        print(f"{i:>2}게임: " + " ".join(f"{n:02d}" for n in g))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
