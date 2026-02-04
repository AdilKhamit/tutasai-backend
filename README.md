# Tutas AI Backend

Базовая структура бекенда на Django + DRF для модулей управления персоналом, объектами, полевыми картами и аналитикой.

## Основные модули
- Users, Qualifications (Auth & HR)
- Contracts, Objects, AccessLetters (Context Data)
- WorkCards, Protocols (Workflow)
- AIAnalysis, ExpertConclusions (Intelligence Layer)
- API витрина для комитета: `/api/dashboard/committee/`
- API кабинет дефектоскописта: `/api/dashboard/inspector/`
- Генерация протокола через ИИ: `/api/protocols/{work_card_id}/generate/`
- Подпись протокола через НЦА (NCALayer): `/api/protocols/{protocol_id}/sign/`

## Быстрый старт
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Документы и OCR
- Генерация PDF: ReportLab или WeasyPrint (подключается на уровне сервисов/фоновых задач).
- OCR/распознавание шильдиков: Tesseract или YOLO (подключается через отдельный сервис/таск).
