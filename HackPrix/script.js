document.addEventListener("DOMContentLoaded", function () {
  // Header scroll behavior
  const header = document.querySelector("header");
  let lastScroll = 0;

  window.addEventListener("scroll", function () {
    const currentScroll = window.pageYOffset;

    if (currentScroll <= 0) {
      header.classList.remove("hidden");
      return;
    }

    if (currentScroll > lastScroll && !header.classList.contains("hidden")) {
      // Scroll down
      header.classList.add("hidden");
    } else if (
      currentScroll < lastScroll &&
      header.classList.contains("hidden")
    ) {
      // Scroll up
      header.classList.remove("hidden");
    }

    lastScroll = currentScroll;
  });

  // Smooth scrolling ONLY for internal anchor links
  document
    .querySelectorAll('a[href^="#"]:not([href="#"])')
    .forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        e.preventDefault();

        const targetElement = document.querySelector(this.getAttribute("href"));
        if (targetElement) {
          window.scrollTo({
            top: targetElement.offsetTop - 80,
            behavior: "smooth",
          });
        }
      });
    });

  // Scroll reveal animation
  function reveal() {
    const reveals = document.querySelectorAll(".reveal");

    for (let i = 0; i < reveals.length; i++) {
      const windowHeight = window.innerHeight;
      const elementTop = reveals[i].getBoundingClientRect().top;
      const elementVisible = 150;

      if (elementTop < windowHeight - elementVisible) {
        reveals[i].classList.add("active");
      } else {
        reveals[i].classList.remove("active");
      }
    }
  }

  window.addEventListener("scroll", reveal);
  reveal(); // Initialize
  // Add click handler to flashcards to ensure they flip and links work
  const flashcards = document.querySelectorAll(".flashcard");
  flashcards.forEach((card, index) => {
    card.style.setProperty("--order", index);
    card.classList.add("reveal", "fade-bottom");

    // Add click to flip functionality for mobile
    card.addEventListener("click", function (e) {
      // If clicking on a link, don't interfere
      if (e.target.tagName === "A" || e.target.closest("a")) {
        return;
      }
      // Toggle flip state for touch devices
      this.classList.toggle("flipped");
    });
  });
  // Add hover effect to buttons only (not links)
  const buttons = document.querySelectorAll(
    "button:not(a), .cta-button:not(a)"
  );
  buttons.forEach((button) => {
    button.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-3px)";
      this.style.boxShadow = "0 8px 15px rgba(0,0,0,0.2)";
    });

    button.addEventListener("mouseleave", function () {
      this.style.transform = "";
      this.style.boxShadow = "";
    });
  });

  // Parallax effect for hero section
  const heroSection = document.querySelector(".hero-section");
  if (heroSection) {
    window.addEventListener("scroll", function () {
      const scrollPosition = window.pageYOffset;
      heroSection.style.backgroundPositionY = scrollPosition * 0.5 + "px";
    });
  }

  // Animate elements when they come into view
  const animateOnScroll = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate_animated", "animate_fadeInUp");
          animateOnScroll.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
    }
  );

  document
    .querySelectorAll(".card-section, .about-section, .affirmation-section")
    .forEach((section) => {
      animateOnScroll.observe(section);
    });
  // Ripple effect for buttons only (not for external links)
  const buttonsWithRipple = document.querySelectorAll(".cta-button");
  buttonsWithRipple.forEach((button) => {
    button.addEventListener("click", function (e) {
      // Only prevent default for buttons without href or with # href
      if (!this.href || this.getAttribute("href") === "#") {
        e.preventDefault();
      }

      const x = e.clientX - e.target.getBoundingClientRect().left;
      const y = e.clientY - e.target.getBoundingClientRect().top;

      const ripple = document.createElement("span");
      ripple.classList.add("ripple");
      ripple.style.left = x + "px";
      ripple.style.top = y + "px";

      this.appendChild(ripple);

      setTimeout(() => {
        ripple.remove();
      }, 1000);
    });
  });
  // Ensure card-back links are clickable - simple approach
  const cardLinks = document.querySelectorAll(".card-back a");
  cardLinks.forEach((link) => {
    // Make sure the links work properly
    link.addEventListener("click", function (e) {
      e.stopPropagation(); // Prevent event bubbling
      // For external links, allow normal behavior
      if (this.href && this.href !== "#" && !this.href.startsWith("#")) {
        console.log("Clicking link:", this.href); // Debug log
        return true; // Allow default behavior
      }
    });

    // Ensure the link is always clickable
    link.style.pointerEvents = "auto";
    link.style.position = "relative";
    link.style.zIndex = "1000";
  });

  // Doula Modal functionality
  const doulaModal = document.getElementById("doula-modal");
  const doulaConnectBtn = document.getElementById("doula-connect-btn");
  const closeModalBtn = document.querySelector(".close");

  // Show modal when Connect button is clicked
  if (doulaConnectBtn) {
    doulaConnectBtn.addEventListener("click", function (e) {
      e.preventDefault();
      doulaModal.style.display = "block";
      document.body.style.overflow = "hidden"; // Prevent background scrolling
    });
  }

  // Close modal when X is clicked
  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", function () {
      doulaModal.style.display = "none";
      document.body.style.overflow = "auto"; // Restore scrolling
    });
  }

  // Close modal when clicking outside of it
  window.addEventListener("click", function (e) {
    if (e.target === doulaModal) {
      doulaModal.style.display = "none";
      document.body.style.overflow = "auto";
    }
  });

  // Simple debug to check if links exist and are clickable
  console.log(
    "Card links found:",
    document.querySelectorAll(".card-back a").length
  );
  document.querySelectorAll(".card-back a").forEach((link, index) => {
    console.log(Link ${index}:, link.href, link.textContent.trim());

    // Ensure links are clickable
    link.style.pointerEvents = "auto";
    link.style.zIndex = "99999";
    link.style.position = "relative";
  });
});

// Function to handle doula option selection
function selectDoulaOption(option) {
  const modal = document.getElementById("doula-modal");

  if (option === "register") {
    alert(
      "Redirecting to Doula Registration Form...\n\nThis would typically open a registration form for doulas to join your platform."
    );
    // You can replace this with actual navigation:
    // window.open('your-doula-registration-url', '_blank');
  } else if (option === "hire") {
    alert(
      "Redirecting to Doula Directory...\n\nThis would typically show a directory of available doulas for hire."
    );
    // You can replace this with actual navigation:
    // window.open('your-doula-directory-url', '_blank');
  }

  // Close modal
  modal.style.display = "none";
  document.body.style.overflow = "auto";
}