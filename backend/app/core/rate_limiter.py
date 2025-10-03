"""
Rate Limiter for Login Attempts
Prevents brute force attacks by limiting failed login attempts
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class LoginAttempt:
    """Record of login attempts for a user"""
    failed_count: int
    locked_until: Optional[datetime]
    last_attempt: datetime


class RateLimiter:
    """
    Simple in-memory rate limiter for login attempts

    Rules:
    - 5 failed attempts within any time period
    - Account locked for 30 minutes after 5 failures
    - Successful login resets the counter
    """

    def __init__(
        self,
        max_attempts: int = 5,
        lockout_duration_minutes: int = 30
    ):
        self.max_attempts = max_attempts
        self.lockout_duration = timedelta(minutes=lockout_duration_minutes)
        self.attempts: Dict[str, LoginAttempt] = {}

    def is_locked(self, username: str) -> bool:
        """Check if account is currently locked"""
        if username not in self.attempts:
            return False

        attempt = self.attempts[username]

        # Check if locked and lock period has expired
        if attempt.locked_until:
            if datetime.now() < attempt.locked_until:
                return True
            else:
                # Lock period expired, reset
                self.reset(username)
                return False

        return False

    def get_lockout_time(self, username: str) -> Optional[datetime]:
        """Get the time when account will be unlocked"""
        if username in self.attempts:
            return self.attempts[username].locked_until
        return None

    def record_failed_attempt(self, username: str) -> None:
        """Record a failed login attempt"""
        now = datetime.now()

        if username not in self.attempts:
            self.attempts[username] = LoginAttempt(
                failed_count=1,
                locked_until=None,
                last_attempt=now
            )
        else:
            attempt = self.attempts[username]
            attempt.failed_count += 1
            attempt.last_attempt = now

            # Lock account if max attempts reached
            if attempt.failed_count >= self.max_attempts:
                attempt.locked_until = now + self.lockout_duration

    def record_successful_login(self, username: str) -> None:
        """Record successful login and reset counter"""
        self.reset(username)

    def reset(self, username: str) -> None:
        """Reset login attempts for a user"""
        if username in self.attempts:
            del self.attempts[username]

    def get_remaining_attempts(self, username: str) -> int:
        """Get number of remaining login attempts"""
        if username not in self.attempts:
            return self.max_attempts

        attempt = self.attempts[username]
        remaining = self.max_attempts - attempt.failed_count
        return max(0, remaining)


# Global rate limiter instance
rate_limiter = RateLimiter(max_attempts=5, lockout_duration_minutes=30)
