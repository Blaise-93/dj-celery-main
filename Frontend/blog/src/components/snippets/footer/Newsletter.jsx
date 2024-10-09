export function Newsletter() {
  return (
    <div>
      <form method="post" action="#" className="footer-box-4">
        <h2 className="footer-box-title">Sign Up for Our Newsletter</h2>
        <p className="newsletter-desc">
          Get limitless updates of our events. Don't miss out.
        </p>
        <div className="sign-up-box">
          <input
            type="email"
            id="userEmail"
            minLength="10"
            name="email"
            className="sign-up"
            placeholder="Enter your email"
            required
          />
          <button type="submit" value="Subscribe" id="submit"
           className="btn">
            Signup
          </button>
        </div>
      </form>
    </div>
  );
}
