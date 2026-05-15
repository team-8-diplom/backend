def account_confirmation_template(confirmation_link: str) -> tuple[str, str]:
    body = (
        '<h3>Welcome!</h3><p>Confirm account: '
        f'<a href="{confirmation_link}">{confirmation_link}</a></p>'
    )
    return ('Confirm your account', body)


def reset_password_template(reset_link: str) -> tuple[str, str]:
    body = (
        '<h3>Password reset</h3><p>Reset password: '
        f'<a href="{reset_link}">{reset_link}</a></p>'
    )
    return ('Reset your password', body)
