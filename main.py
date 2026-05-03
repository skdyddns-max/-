#!/usr/bin/env python3
import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from src.card_maker import CardMaker


def main():
    parser = argparse.ArgumentParser(description="뉴스 카드뉴스 자동 생성기")
    parser.add_argument("--category", default="it", choices=["it", "economy"], help="뉴스 카테고리 (기본값: it)")
    parser.add_argument("--count", type=int, default=1, help="생성할 카드뉴스 수 (기본값: 1)")
    parser.add_argument("--demo", action="store_true", help="샘플 데이터로 카드 이미지 생성 테스트")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  카드뉴스 자동 생성기")
    print(f"  카테고리: {args.category} | 개수: {args.count}")
    if args.demo:
        print(f"  모드: 데모 (샘플 데이터)")
    print(f"{'='*50}\n")

    if args.demo:
        _run_demo(args.category)
        return

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("오류: ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 생성하고 API 키를 설정해주세요.")
        print("  cp .env.example .env")
        sys.exit(1)

    from src.crawler import crawl_naver_news
    from src.generator import generate_card_content

    print("📰 뉴스 크롤링 중...")
    articles = crawl_naver_news(args.category, args.count)

    if not articles:
        print("크롤링된 뉴스가 없습니다.")
        sys.exit(1)

    print(f"  {len(articles)}개 기사 수집 완료\n")

    for i, article in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}] {article['title'][:40]}...")
        print("  ✍️  카드뉴스 텍스트 생성 중...")
        card_content = generate_card_content(article)

        print("  🎨  카드 이미지 생성 중...")
        maker = CardMaker(category=args.category)
        out_dir = maker.create_cards(article, card_content)

        print(f"  ✅  완료 → {out_dir}\n")

    print("모든 카드뉴스 생성이 완료되었습니다!")
    print("output/ 폴더를 확인해주세요.")


def _run_demo(category: str):
    from src.demo_data import DEMO_ARTICLE, DEMO_CARD_CONTENT

    print("🎨  데모 카드 이미지 생성 중...")
    maker = CardMaker(category=category)
    out_dir = maker.create_cards(DEMO_ARTICLE, DEMO_CARD_CONTENT)
    print(f"\n✅  완료 → {out_dir}")
    print("output/ 폴더를 확인해주세요.")


if __name__ == "__main__":
    main()
