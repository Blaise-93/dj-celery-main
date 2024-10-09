import AppBar from "@mui/material/AppBar";
import Button from "@mui/material/Button";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import CssBaseline from "@mui/material/CssBaseline";
import companyLogo from '../assets/company/Blaisemart.jpg'


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
            <li>Blog</li>
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
