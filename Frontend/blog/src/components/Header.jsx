import companyLogo from '../assets/company/Blaisemart.jpg'
import {NavLink} from 'react-router-dom'

function Header() {
  return (
    <div className="container">
      <div className="navbar-container">
        <div className="navbar-left-items items">
          <div className='image-container'>
            <a href="#" className="homepage">
              <img src={companyLogo} className="company-logo" alt="company logo" />
              Blaisemart
            </a>
          </div>
          <ul>
            <li>Home</li>
            <li>Pricing</li>
            <li><a href='/'>Blog</a></li>
          </ul>
        </div>
        {/* <div className="navbar-right-items items">
          <ul>
            <li>Contact Us</li>
            <li>Login</li>
            <li>Logout</li>
            <li>Signup</li>
          </ul>
        </div> */}
      </div>
    </div>
  );
}

export default Header;
