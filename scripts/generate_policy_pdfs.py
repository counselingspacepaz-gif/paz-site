from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
CONTENTS = ROOT / "contents"
LOGO = ROOT / "images" / "logo" / "paz-logo.png"
FONT = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")

pdfmetrics.registerFont(TTFont("PazJP", str(FONT)))
pdfmetrics.registerFontFamily("PazJP", normal="PazJP", bold="PazJP")

PAGE_W, PAGE_H = A4
BLUE = colors.HexColor("#17628A")
GREEN = colors.HexColor("#7D946F")
TEXT = colors.HexColor("#222222")
LIGHT = colors.HexColor("#F5F7F4")

styles = getSampleStyleSheet()
base = ParagraphStyle(
    "BaseJP",
    parent=styles["BodyText"],
    fontName="PazJP",
    fontSize=8.0,
    leading=11.4,
    textColor=TEXT,
    spaceAfter=3,
    wordWrap="CJK",
)
small = ParagraphStyle("SmallJP", parent=base, fontSize=7.1, leading=9.6)
title = ParagraphStyle(
    "TitleJP",
    parent=base,
    fontSize=20,
    leading=24,
    alignment=TA_CENTER,
    spaceAfter=9,
)
section = ParagraphStyle(
    "SectionJP",
    parent=base,
    fontSize=10.8,
    leading=13,
    textColor=BLUE,
    spaceBefore=5,
    spaceAfter=2,
)
policy_section = ParagraphStyle(
    "PolicySectionJP",
    parent=section,
    fontSize=10.2,
    leading=12,
    textColor=GREEN,
)
right = ParagraphStyle("RightJP", parent=small, alignment=TA_RIGHT)
center_small = ParagraphStyle("CenterSmallJP", parent=small, alignment=TA_CENTER)


def header():
    logo = Image(str(LOGO), width=34 * mm, height=22 * mm, kind="proportional")
    contact = Paragraph(
        "カウンセリングスペース paz<br/>"
        "〒410-0801 静岡県沼津市大手町4-3-28 リバーサイド大手町502<br/>"
        "メール：info@counselingspacepaz.com<br/>"
        "Webサイト：https://counselingspacepaz.com",
        right,
    )
    table = Table([[logo, contact]], colWidths=[44 * mm, 116 * mm])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def bullet_list(items, style=base, left=13):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=0) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=left,
        bulletFontName="PazJP",
        bulletFontSize=6,
        spaceAfter=2,
    )


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("PazJP", 7)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawCentredString(PAGE_W / 2, 6 * mm, f"{doc.page}")
    canvas.restoreState()


def make_terms():
    path = CONTENTS / "terms-of-service-inperson.pdf"
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=9 * mm,
        bottomMargin=10 * mm,
        title="Counseling Space paz カウンセリング同意書",
        author="Counseling Space paz",
    )
    story = [header(), Spacer(1, 2 * mm), Paragraph("カウンセリング同意書", title)]
    story.append(Paragraph("年　　　月　　　日", right))

    sections = [
        (
            "カウンセリングの性質について",
            "当施設で提供するカウンセリングは医療行為ではありません。必要に応じて、医療機関との連携や受診をお勧めする場合があります。現在、精神科・心療内科等に通院中の方は、主治医の承諾書をご提出ください。",
        ),
        (
            "予約変更・キャンセルについて",
            "予約変更・キャンセル、当日のご連絡は、メールまたはLINEでお知らせください。受付時刻はメッセージの送信日時を基準とします。2026年12月1日以降に確定するご予約には、次のポリシーを適用します。2026年11月30日以前に確定したご予約には従来のルールを適用します。",
        ),
    ]
    for heading, body in sections:
        story.extend([Paragraph(heading, section), Paragraph(body, base)])

    policy_data = [
        [Paragraph("ご連絡の時期", small), Paragraph("取り扱い", small)],
        [Paragraph("面接日の2日前まで", small), Paragraph("変更・キャンセルとも無料（振替先が未定でも無料）", small)],
        [Paragraph("面接日の前日", small), Paragraph("キャンセル50％。3日以内に返信があり、具体的な日程調整が進んでいる予約変更は無料。返信がないとき、または日程調整が進まず変更不成立の場合は50％", small)],
        [Paragraph("面接日当日", small), Paragraph("変更・キャンセルとも100％", small)],
        [Paragraph("無断キャンセル", small), Paragraph("100％", small)],
    ]
    table = Table(policy_data, colWidths=[42 * mm, 118 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#BBBBBB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.extend(
        [
            table,
            Paragraph(
                "キャンセル料は予約された面接料金を基準に算定します。「前日」「2日前まで」は暦日で判断し、面接日前日の0:00〜23:59を前日として扱います。",
                small,
            ),
            Paragraph("前日の予約変更", policy_section),
            Paragraph(
                "前日の変更は、候補日の案内から3日以内（暦日）に返信があり、具体的な日程調整が進んでいる場合は無料です。返信後、pazからの案内を待つ間は利用者の返信期限を進めません。新しい候補をお送りした場合は再び3日間の期限を設けます。pazからの確認返信をもって振替日時が確定します。所定の期限内に返信がないとき、または具体的な日程調整が進まず予約変更が不成立となったときは、最初のお申し出の送信日時を基準にキャンセル料を算定します。pazからの返信が翌日以降になった場合や休業日を挟んだ場合も同様です。",
                small,
            ),
            Paragraph(
                "paz側の事情で振替日時をご案内できない場合はキャンセル料をいただきません。体調不良・災害等のやむを得ない事情は個別にご相談ください。詳細は https://counselingspacepaz.com/booking/ をご確認ください。",
                small,
            ),
            Paragraph("カウンセリングの終了について", section),
            Paragraph("終了を希望される場合は、メールまたはLINEでご連絡ください。連絡がないままキャンセルされた場合は、規定に基づきキャンセル料が発生します。", base),
            Paragraph("安全と倫理の遵守", section),
            Paragraph("カウンセラーに対する暴力・脅迫・その他の犯罪行為があった場合、カウンセリングを継続できません。必要に応じて関係機関へ通報する場合があります。", base),
            Paragraph("記録・録音について", section),
            Paragraph("支援の質向上のため面接場面を録音する場合があります。録音の際は事前に説明し、同意を得ます。", base),
            Paragraph("プライバシーと個人情報の保護", section),
            Paragraph("当施設は公認心理師法に基づく守秘義務を遵守します。原則として、利用者の同意なく第三者へ個人情報を開示しません。ただし法令に基づく場合や、生命・安全に関わる緊急事態には適切な対応を取ることがあります。", base),
            Paragraph("※18歳未満の利用者は、保護者の同意が必要です。", small),
            Spacer(1, 2 * mm),
            Paragraph("以上に同意し、カウンセリングを利用いたします。", base),
            Spacer(1, 2 * mm),
        ]
    )

    signature = Table(
        [
            [Paragraph("利用者　　　　　　　　　　　　　　　　　印", base), Paragraph("保護者　　　　　　　　　　　　　　　　　印", base)],
            [Paragraph("住所　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　", base), ""],
            [Paragraph("担当者　　　　　　　　　　　　　　　　　印", base), Paragraph("年　　　　　月　　　　　日", base)],
        ],
        colWidths=[80 * mm, 80 * mm],
    )
    signature.setStyle(
        TableStyle(
            [
                ("SPAN", (0, 1), (1, 1)),
                ("LINEBELOW", (0, 0), (-1, -1), 0.35, colors.HexColor("#555555")),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(signature)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def make_privacy():
    path = CONTENTS / "privacy-policy-paz.pdf"
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=9 * mm,
        bottomMargin=10 * mm,
        title="Counseling Space paz プライバシーポリシー",
        author="Counseling Space paz",
    )
    story = [
        Paragraph("プライバシーポリシー", title),
        Paragraph("Counseling Space paz｜https://counselingspacepaz.com", center_small),
        Spacer(1, 1 * mm),
    ]

    # 正常な旧版の9項目構成と本文を維持し、連絡先の変更と
    # Google Analytics 4の利用についてのみ必要最小限を追記する。
    blocks = [
        ("1．基本方針", "当施設は、個人情報保護法、公認心理師法、臨床心理士倫理綱領に基づき、相談者の個人情報を適切に管理します。利用目的を明確にし、最小限必要な範囲で取り扱います。"),
        ("2．取得する情報", None),
        ("3．利用目的", None),
        ("4．第三者提供・委託", None),
        ("5．安全管理措置", None),
        ("6．利用者の権利", None),
        ("7．例外的な情報共有", None),
        ("8．未成年の利用", None),
        ("9．制定日・改定日", None),
    ]

    collected = [
        "氏名、年齢、連絡先（メール・LINE）",
        "予約情報（日時、サービス内容）",
        "相談内容に関する記録（要約）",
    ]
    purposes = [
        "相談支援の実施および予約管理",
        "必要な連絡（リマインド、変更・緊急連絡）",
        "サービス運営・品質向上のための最小限の分析",
        "法令等に基づく対応",
    ]
    third_party = [
        "本人同意なしに第三者提供は行いません。",
        "例外：法令に基づく場合、生命・身体の危険がある場合。",
        "Microsoft 365（Microsoft Bookings等）を利用し、国外サーバでデータが扱われる可能性があります。",
        "当サイトではGoogle Analytics 4を利用します。Cookie等によるアクセス情報は、サイトの利用状況の把握と改善のために使用します。",
    ]

    security = ["アクセス制御、パスワード管理、施錠保管", "必要に応じて暗号化・ログ管理", "運用状況の定期的な見直し"]
    rights = ["本人確認の上、開示・訂正・削除・利用停止の請求に対応します。", "ただし、法令や安全確保のために必要な場合は応じられないことがあります。"]
    exceptions = ["生命・身体の安全が差し迫る場合", "法令に基づく照会や開示要請", "医療機関等との連携が必要で迅速な対応が求められる場合"]
    minors = ["18歳未満は保護者の同意必須", "15歳以下は対象（当施設の方針）"]
    dates = ["制定日：2025年10月31日", "最終改定日：2026年11月9日"]

    for heading, body in blocks:
        story.append(Paragraph(heading, policy_section))
        if body:
            story.append(Paragraph(body, base))
        if heading.startswith("2．"):
            story.append(bullet_list(collected, small))
        elif heading.startswith("3．"):
            story.append(bullet_list(purposes, small))
        elif heading.startswith("4．"):
            story.append(bullet_list(third_party, small))
        elif heading.startswith("5．"):
            story.append(bullet_list(security, small))
        elif heading.startswith("6．"):
            story.append(bullet_list(rights, small))
        elif heading.startswith("7．"):
            story.append(bullet_list(exceptions, small))
        elif heading.startswith("8．"):
            story.append(bullet_list(minors, small))
        elif heading.startswith("9．"):
            story.append(bullet_list(dates, small))

    story.extend(
        [
            Spacer(1, 2 * mm),
        ]
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    make_terms()
    make_privacy()
