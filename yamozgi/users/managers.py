from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_some_user(self, email, login, password, **extra_fields):

        if not email:
            raise ValueError('Необходимо указать почту')
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            login=login,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, login, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self.create_some_user(email, login, password, **extra_fields)

    def create_superuser(self, email, login, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_some_user(email, login, password, **extra_fields)
