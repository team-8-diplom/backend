from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')


def account_confirmation_template(confirmation_link: str) -> tuple[str, str]:
    subject = 'Подтверждение регистрации'
    template = templates.get_template('account_confirmation.html')
    body = template.render(confirmation_link=confirmation_link)

    return (subject, body)


def reset_password_template(reset_link: str) -> tuple[str, str]:
    subject = 'Восстановление пароля'
    template = templates.get_template('reset_password.html')
    body = template.render(reset_link=reset_link)

    return (subject, body)
