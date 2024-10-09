import Copyright  from "./snippets/footer/copyright";
import { Newsletter } from "./snippets/footer/Newsletter";
import Gallery from "./snippets/footer/Gallery";

function Footer() {
  return (
    <div className="footer-containers pb-16">
      <div className="container-one">
        <div className="footer-box-1">
          <h2 className="footer-box-title">Contact Details</h2>
          <p className="box-1-item">
            <i
              className="fa-sharp fa-solid fa-location-dot detail-icon"
              aria-label="location icon"
            ></i>{" "}
            17 Adeleke St, Allen Ave, Allen Ikeja 100271, Lagos Ikeja, Lagos,
            Nigeria
          </p>
          <p className="box-1-item">
            <i
              className="fa-sharp fa-solid fa-phone detail-icon"
              aria-label="phone icon"
            ></i>{" "}
            +234 913 565 9696{" "}
          </p>
          <p className="box-1-item">
            <i
              className="fa-solid fa-envelope-open detail-icon"
              aria-label="message icon"
            ></i>{" "}
            Oririrestaurant5@gmail.com
          </p>
          <p className="box-1-item">
            <i
              className="fa-solid fa-clock detail-icon"
              aria-label="time opening icon"
            ></i>
            Opening Hours: Monday to Sunday (10am to 9pm)
          </p>
          <div className="socials">
            <div className=" linkedin">
              <a
                href="https://github.com/Blaise-93/pharmcare"
                target="_blank"
                className="social-icon"
                aria-label="linkedin social media icon"
              >
                <i
                  className="fa-brands fa-linkedin detail-icon"
                  aria-label="linkedin social media icon"
                ></i>
              </a>
            </div>
            <div className="facebook">
              <a
                href="https://github.com/Blaise-93/pharmcare"
                target="_blank"
                className="social-icon"
                aria-label="facebook social media icon"
              >
                <i
                  className="fa-brands fa-facebook detail-icon"
                  aria-label="facebook social media icon"
                ></i>
              </a>
            </div>
            <div className="instagram">
              <a
                href="https://github.com/Blaise-93/pharmcare"
                target="_blank"
                className="social-icon"
                aria-label="instagram social media icon"
              >
                <i
                  className="fa-brands fa-instagram detail-icon"
                  aria-label="instagram social media icon"
                ></i>
              </a>
            </div>
            <div className="twitter">
              <a
                href="https://github.com/Blaise-93/pharmcare"
                target="_blank"
                className="social-icon"
                aria-label="twitter social media icon"
              >
                <i
                  className="fa-brands fa-x-twitter detail-icon"
                  aria-label="twitter social media icon"
                ></i>
              </a>
            </div>
          </div>
        </div>
        <div className="footer-box-2">
          <h2 className="footer-box-title">
            <span className="company">Company</span>
          </h2>
          <ul className="footer-box-items-1">
            <li className="box-1-item location">
              <a href="" className="useful-links-item">
                <i
                  className="fa-solid fa-mobile-screen"
                  aria-label="company useful links"
                ></i>{" "}
                About Us
              </a>
            </li>
            <li className="box-1-item">
              <a href="" className="useful-links-item">
                <i
                  className="fa-solid fa-mobile-screen"
                  aria-label="company useful links"
                ></i>{" "}
                Our Services
              </a>{" "}
            </li>
            <li className="box-1-item">
              <a href="" className="useful-links-item">
                <i
                  className="fa-solid fa-mobile-screen"
                  aria-label="company useful links"
                ></i>{" "}
                Management
              </a>{" "}
            </li>
            <li className="box-1-item">
              <a href="" className="useful-links-item">
                <i
                  className="fa-solid fa-mobile-screen"
                  aria-label="company useful links"
                ></i>{" "}
                Contact Us
              </a>
            </li>
            <li className="box-1-item">
              <a href="" className="useful-links-item">
                <i
                  className="fa-solid fa-mobile-screen"
                  aria-label="company useful links"
                ></i>{" "}
                Privacy Policy
              </a>
            </li>
            <li className="box-1-item">
              <a href="" className="useful-links-item">
                <i
                  className="fa-solid fa-mobile-screen"
                  aria-label="company useful links"
                ></i>{" "}
                Terms of Services
              </a>
            </li>
          </ul>
        </div>
        <div>
        <Gallery />
        <Newsletter />
        <Copyright />
        </div>
       
      </div>
    </div>
  );
}

export default  Footer;