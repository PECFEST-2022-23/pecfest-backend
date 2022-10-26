during register
registered -> send it to login
unverified -> backend -> send email, frontend -> plz click on link provided on email

during login
!registered -> send to sign up flow
registered && !verified -> backend -> send email, frontend -> plz click on link provided on email
registered && verified -> additional detail (backend->send token)
completed -> (backend->send token)

1. redirect 400
2. unverfied
3. verified
4. completed
5. incorrect_data 400

pecfest.co.in/api/verifiy/djnsdivbdfijbvefbui/

backend/auth/verify/ data = {token:sdjbsdibeihu}
response: 1. verified and to be verify -> accound verified msg: "account verified" 2. link expired -> show button to redirect to login msg: "link expired"

forgot password on login:
enter email and new password -> POST email and new pass
backend-> email+newpass -> token -> send email

    pecfest.co.in/api/reset-pass/token/
    backend/auth/reset-pass/  data = {token:sjdfbsifew}

    response: your password updated please login again button
