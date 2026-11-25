# Архитектура обработки событий

```mermaid
flowchart LR
  User[Учебный пользователь] --> App[PHP TimeCapsule]
  App -->|capsule.sealed| Topic[SNS events]
  Topic --> Queue[SQS mail]
  Queue -.->|Необработанные записи| DLQ[SQS DLQ]
  Queue --> Mailer[Lambda mailer]
  Mailer -->|TLS и дедупликация| DB[(Учебная PostgreSQL)]
  Scheduler[EventBridge Scheduler] --> Opener[Lambda opener]
  Opener -->|TLS и обновление opened_at| DB
  Opener -->|OnSuccess| Open[SNS opened]
  Open --> Proof[SQS для проверки назначения]
  Mailer --> CW[CloudWatch Logs]
  Opener --> CW
```

Lambda запускались в приватных подсетях учебной VPC. Для сквозного прогона PostgreSQL работала на EC2. Успешное назначение проверено через SQS, подписанную на SNS. Email в этом прогоне не отправлялся.
