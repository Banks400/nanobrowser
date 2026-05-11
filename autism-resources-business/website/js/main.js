/* ============================================
   SPECTRUMREADY — MAIN JAVASCRIPT
   ============================================ */

/* ---------- LEAD FORM ---------- */
function handleLeadForm(event) {
  event.preventDefault();

  const form = document.getElementById('leadForm');
  const successDiv = document.getElementById('formSuccess');
  const firstName = document.getElementById('firstName').value;
  const email = document.getElementById('email').value;

  // --- INTEGRATION POINT ---
  // Replace this block with your actual email platform integration.
  // Options:
  //   ConvertKit: POST to https://app.convertkit.com/forms/YOUR_FORM_ID/subscriptions
  //   MailerLite:  POST to https://api.mailerlite.com/api/v2/subscribers
  //   ActiveCampaign: POST to your AC form action URL
  //
  // Example ConvertKit fetch:
  //
  // fetch('https://app.convertkit.com/forms/YOUR_FORM_ID/subscriptions', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ email_address: email, first_name: firstName }),
  // });

  console.log('Lead captured:', { firstName, email });

  // Show success state
  form.classList.add('hidden');
  successDiv.classList.remove('hidden');

  // Track conversion event (Google Analytics / Facebook Pixel)
  if (typeof gtag !== 'undefined') {
    gtag('event', 'lead_magnet_signup', { email, first_name: firstName });
  }

  if (typeof fbq !== 'undefined') {
    fbq('track', 'Lead', { content_name: 'free_guide_5_programs' });
  }
}

/* ---------- PURCHASE HANDLER ---------- */
const PRODUCTS = {
  bundle: {
    name: 'The Complete Autism Parent Toolkit',
    price: 127,
    // Replace with your Stripe payment link or Stan Store product URL
    url: 'https://buy.stripe.com/YOUR_BUNDLE_LINK',
  },
  benefits: {
    name: 'The Autism Benefits Navigator',
    price: 47,
    url: 'https://buy.stripe.com/YOUR_BENEFITS_LINK',
  },
  iep: {
    name: 'IEP Mastery: The Parent\'s Advocacy Bible',
    price: 47,
    url: 'https://buy.stripe.com/YOUR_IEP_LINK',
  },
  therapy: {
    name: 'The Complete Therapy Roadmap',
    price: 47,
    url: 'https://buy.stripe.com/YOUR_THERAPY_LINK',
  },
  insurance: {
    name: 'The Autism Insurance Battle Guide',
    price: 37,
    url: 'https://buy.stripe.com/YOUR_INSURANCE_LINK',
  },
  diagnosis: {
    name: 'Navigating the Diagnosis Journey',
    price: 37,
    url: 'https://buy.stripe.com/YOUR_DIAGNOSIS_LINK',
  },
  transition: {
    name: 'Transition to Adulthood Planner',
    price: 47,
    url: 'https://buy.stripe.com/YOUR_TRANSITION_LINK',
  },
};

function handlePurchase(productKey) {
  const product = PRODUCTS[productKey];
  if (!product) return;

  // Track purchase intent (analytics)
  if (typeof gtag !== 'undefined') {
    gtag('event', 'begin_checkout', {
      currency: 'USD',
      value: product.price,
      items: [{ item_name: product.name, price: product.price }],
    });
  }

  if (typeof fbq !== 'undefined') {
    fbq('track', 'InitiateCheckout', {
      content_name: product.name,
      value: product.price,
      currency: 'USD',
    });
  }

  // Redirect to payment page
  // For Stan Store / Gumroad: replace product.url with your product checkout URL
  window.location.href = product.url;
}

/* ---------- FAQ ACCORDION ---------- */
function toggleFaq(button) {
  const answer = button.nextElementSibling;
  const isOpen = button.classList.contains('open');

  // Close all
  document.querySelectorAll('.faq-question.open').forEach((btn) => {
    btn.classList.remove('open');
    btn.nextElementSibling.classList.remove('open');
  });

  // Open clicked (if it was closed)
  if (!isOpen) {
    button.classList.add('open');
    answer.classList.add('open');
  }
}

/* ---------- MOBILE NAV ---------- */
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const isOpen = navLinks.style.display === 'flex';
    navLinks.style.display = isOpen ? '' : 'flex';
    navLinks.style.flexDirection = isOpen ? '' : 'column';
    navLinks.style.position = isOpen ? '' : 'absolute';
    navLinks.style.top = isOpen ? '' : '68px';
    navLinks.style.left = isOpen ? '' : '0';
    navLinks.style.right = isOpen ? '' : '0';
    navLinks.style.background = isOpen ? '' : 'white';
    navLinks.style.padding = isOpen ? '' : '20px 24px';
    navLinks.style.boxShadow = isOpen ? '' : '0 4px 6px rgba(0,0,0,0.1)';
    navLinks.style.zIndex = isOpen ? '' : '99';
  });
}

/* ---------- STICKY NAV SCROLL ---------- */
const navbar = document.querySelector('.navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.style.boxShadow =
      window.scrollY > 10 ? '0 4px 6px -1px rgba(0,0,0,0.1)' : 'none';
  });
}

/* ---------- SMOOTH SCROLL FOR ANCHOR LINKS ---------- */
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', (e) => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    const offset = 80;
    const top = target.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top, behavior: 'smooth' });

    // Close mobile nav if open
    if (navLinks) navLinks.style.display = '';
  });
});

/* ---------- INTERSECTION OBSERVER (fade-in animations) ---------- */
const observeElements = document.querySelectorAll(
  '.product-card, .testimonial-card, .pain-card, .faq-item',
);

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 },
  );

  observeElements.forEach((el) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });
}
