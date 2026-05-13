def account_confirmation_template(confirmation_link: str) -> tuple[str, str]:
    return (
        'Confirm your account',
        f'<h3>Welcome!</h3><p>Confirm account: <a href="{confirmation_link}">{confirmation_link}</a></p>',
    )


def reset_password_template(reset_link: str) -> tuple[str, str]:
    return (
        'Reset your password',
        f'<h3>Password reset</h3><p>Reset password: <a href="{reset_link}">{reset_link}</a></p>',
    )
