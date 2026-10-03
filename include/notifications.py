from html import escape

from airflow.utils.email import send_email


EMAIL_TO = "tonymiguel71@gmail.com"


def _format_duration(start, end):
    if not start or not end:
        return "Não disponível"

    seconds = int((end - start).total_seconds())
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours:
        return f"{hours}h {minutes}min {seconds}s"
    if minutes:
        return f"{minutes}min {seconds}s"
    return f"{seconds}s"


def _send_notification(context, status):
    dag_run = context.get("dag_run")
    dag = context.get("dag")
    task_instance = context.get("task_instance")

    dag_id = dag.dag_id if dag else "N/A"

    start_date = dag_run.start_date if dag_run else None
    end_date = dag_run.end_date if dag_run else None

    duration = _format_duration(start_date, end_date)

    failed_task = "Nenhuma"

    if dag_run:
        try:
            failed_tasks = [
                ti.task_id
                for ti in dag_run.get_task_instances()
                if ti.state == "failed"
            ]

            if failed_tasks:
                failed_task = ", ".join(failed_tasks)
        except Exception:
            failed_task = (
                task_instance.task_id
                if task_instance
                else "Não identificado"
            )

    subject = f"[Projeto 2] Pipeline {status}: {dag_id}"

    html_content = f"""
    <html>
        <body>
            <h2>Pipeline {escape(status)}</h2>

            <p><strong>Pipeline:</strong> {escape(dag_id)}</p>
            <p><strong>Status:</strong> {escape(status)}</p>
            <p><strong>Início:</strong> {escape(str(start_date or "N/A"))}</p>
            <p><strong>Fim:</strong> {escape(str(end_date or "N/A"))}</p>
            <p><strong>Duração:</strong> {escape(duration)}</p>
            <p><strong>Task com falha:</strong> {escape(failed_task)}</p>
        </body>
    </html>
    """

    send_email(
        to=EMAIL_TO,
        subject=subject,
        html_content=html_content,
    )


def notify_success(context):
    _send_notification(context, "SUCESSO")


def notify_failure(context):
    _send_notification(context, "FALHA")
