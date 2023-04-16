import classes from './Login.module.css'

function Login() {
  return (
    <div className={classes.container}>
      <h1 class="title">Textbook Exchange System</h1>
      <form class="form" method="POST" action="/login">
        <div class="form-group">
          <label for="username">Account:</label>
          <input type="text" id="username" name="username" required />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" name="password" required />
        </div>
        <div class="form-group">
          <input type="submit" value="Login" />
        </div>
      </form>

      <button class="signup" onclick="location.href=`{{ url_for('signup') }}`">
        Signup
      </button>

      <div class="form-group alt-link">
        <a href="#">Forgot password?</a>
      </div>
      {/* <!--      <form class="form" method="POST" action="/login">-->
  <!--&lt;!&ndash;      <form class="form">&ndash;&gt;-->
  <!--        <div class="form-group">-->
  <!--          <label for="username">Account:</label>-->
  <!--          <input type="text" id="username" name="username" required>-->
  <!--        </div>-->
  <!--        <div class="form-group">-->
  <!--          <label for="password">Password:</label>-->
  <!--          <input type="password" id="password" name="password" required>-->
  <!--        </div>-->
  <!--        <div class="form-group">-->
  <!--          <input type="submit" value="Login">-->
  <!--        </div>-->
  <!--        <div class="form-group">-->
  <!--          <input type="submit" value="Sign Up">-->
  <!--        </div>-->
  <!--        <div class="form-group alt-link">-->
  <!--          <a href="#">Forgot password?</a>-->
  <!--        </div>-->
  <!--      </form>--> */}
    </div>
  )
}

export default Login
