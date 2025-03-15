document.addEventListener("DOMContentLoaded", function () {
  const images = [
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1718741635/womendress_z7tivy.png", alt: "womens", label: "Womens" },
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1718741636/womenshoes_hyfgev.png", alt: "shoes", label: "Shoes" },
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1718741635/kids_myt7n6.png", alt: "kids", label: "Kids" },
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1718741619/jewelries_tax5mp.png", alt: "accessories", label: "Accessories" },
    { src: "https://res.cloudinary.com/dns8ckviy/image/upload/v1718741635/womenbeauty_efrdxz.png", alt: "beauty", label: "Beauty" },
    // Add more images as needed
  ];

  // Select the container element
  const container = document.getElementById("categories");

  // Loop through the array and create HTML elements
  if (container) {
    images.forEach((image) => {
      const imageWrapper = document.createElement("div");
      imageWrapper.className = "category_card";

      const imageContainer = document.createElement("a");
      imageContainer.className = "category_card--image-container";
      // Set the href attribute
      imageContainer.href = "/catalog?product_name="+image.alt;

      const img = document.createElement("img");
      img.src = image.src;
      img.alt = image.alt;
      img.className = "category_card--img";

      const label = document.createElement("h4");
      label.className = "category_card--label";
      label.textContent = image.label;

      imageContainer.appendChild(img);
      imageWrapper.appendChild(imageContainer);
      imageWrapper.appendChild(label);
      container.appendChild(imageWrapper);
    });
  }
  const overlay = document.getElementById('overlay');
  const open_cart = document.getElementById('open_cart');
  const open_mobile_cart = document.getElementById('open_mobile_cart');
  const close_cart = document.getElementById('close_cart');
  const cart_box = document.querySelector('#cart_box');

  // Show the cart popup
  open_cart.addEventListener('click', () => {
      cart_box.style.display = 'block';  // Show the cart box
      overlay.classList.add('active');;  /* Semi-transparent black */
      // console.log("Opencart")
  });

  open_mobile_cart.addEventListener('click', () => {
    cart_box.style.display = 'block';  // Show the cart box
    overlay.classList.add('active');;  /* Semi-transparent black */
    // console.log("Opencart")
});

  // Close the cart popup
  close_cart.addEventListener('click', () => {
      cart_box.style.display = 'none';  // Hide the cart box
      overlay.classList.remove('active')
      // console.log("closecart")
  });

  // Optional: Close the cart box if the user clicks outside the popup
  document.addEventListener('click', (event) => {
    // Check if the click is outside the cart and overlay
    if (!cart_box.contains(event.target) && overlay.contains(event.target) && !open_cart.contains(event.target) && !open_moible_cart.contains(event.target)) {
      cart_box.style.display = 'none';  // Hide the cart box
      overlay.classList.remove('active');  // Hide the overlay
    }
  });










  // product-dropdown
  document
    .getElementById("product-dropdown")
    .addEventListener("click", function () {
      const dropdownContent = document.getElementById(
        "product-dropdown-content",
      );
      dropdownContent.classList.toggle("hidden");
      document
        .querySelector("#product-dropdown i")
        .classList.toggle("fa-angle-down");
      document
        .querySelector("#product-dropdown i")
        .classList.toggle("fa-angle-up");
    });

  // size-dropdown
  document
    .getElementById("size-dropdown")
    .addEventListener("click", function () {
      const dropdownContent = document.getElementById("size-dropdown-content");
      dropdownContent.classList.toggle("hidden");
      document
        .querySelector("#size-dropdown i")
        .classList.toggle("fa-angle-down");
      document
        .querySelector("#size-dropdown i")
        .classList.toggle("fa-angle-up");
    });

  let rangeMin = 100;
  const range = document.querySelector(".range-selected");
  const rangeInput = document.querySelectorAll(".range-input input");
  const rangePrice = document.querySelectorAll(".range-price input");

  rangeInput.forEach((input) => {
    input.addEventListener("input", (e) => {
      let minRange = parseInt(rangeInput[0].value);
      let maxRange = parseInt(rangeInput[1].value);
      if (maxRange - minRange < rangeMin) {
        if (e.target.className === "min") {
          rangeInput[0].value = maxRange - rangeMin;
        } else {
          rangeInput[1].value = minRange + rangeMin;
        }
      } else {
        rangePrice[0].value = minRange;
        rangePrice[1].value = maxRange;
        range.style.left = (minRange / rangeInput[0].max) * 100 + "%";
        range.style.right = 100 - (maxRange / rangeInput[1].max) * 100 + "%";
      }
    });
  });

  rangePrice.forEach((input) => {
    input.addEventListener("input", (e) => {
      let minPrice = rangePrice[0].value;
      let maxPrice = rangePrice[1].value;
      if (maxPrice - minPrice >= rangeMin && maxPrice <= rangeInput[1].max) {
        if (e.target.className === "min") {
          rangeInput[0].value = minPrice;
          range.style.left = (minPrice / rangeInput[0].max) * 100 + "%";
        } else {
          rangeInput[1].value = maxPrice;
          range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
        }
      }
    });
  });
});



// Function to remove query arguments from the browser URL
function removeArgsFromBrowserUrl() {
    const currentUrl = window.location.href;
    const baseUrl = currentUrl.split('?')[0]; // Get the URL without query parameters

    // Update the browser's URL without reloading the page
    history.replaceState(null, '', baseUrl);
    location.reload();
}

// Add an event listener to the button
document.getElementById("removeArgsButton").addEventListener("click", removeArgsFromBrowserUrl);


 // Get references to the inputs and sliders
 const minInput = document.getElementById('minInput');
 const maxInput = document.getElementById('maxInput');
 const minRange = document.getElementById('minRange');
 const maxRange = document.getElementById('maxRange');

 // Synchronize slider and input for the minimum price
 minRange.addEventListener('input', () => {
   minInput.value = minRange.value;
   if (parseInt(minRange.value) > parseInt(maxRange.value)) {
     maxRange.value = minRange.value;
     maxInput.value = minRange.value;
   }
 });

 minInput.addEventListener('input', () => {
   const value = parseInt(minInput.value) || 0;
   minRange.value = value;
   if (value > parseInt(maxRange.value)) {
     maxRange.value = value;
     maxInput.value = value;
   }
 });

 // Synchronize slider and input for the maximum price
 maxRange.addEventListener('input', () => {
   maxInput.value = maxRange.value;
   if (parseInt(maxRange.value) < parseInt(minRange.value)) {
     minRange.value = maxRange.value;
     minInput.value = maxRange.value;
   }
 });

 maxInput.addEventListener('input', () => {
   const value = parseInt(maxInput.value) || 0;
   maxRange.value = value;
   if (value < parseInt(minRange.value)) {
     minRange.value = value;
     minInput.value = value;
   }
 });



 function updatePageNumber(pageNum) {
  const url = new URL(window.location.href); // Get the current URL
  url.searchParams.set('page_num', pageNum); // Add or update the 'page_num' parameter
  window.location.href = url.toString(); // Redirect to the updated URL
}

function updatePageNumber_nextButton() {
  let pgN = document.getElementById('pgN')
  const url = new URL(window.location.href); // Get the current URL
  
  // Get the current 'page_num' value from the URL (default to 1 if not present)
  let pageNum = parseInt(url.searchParams.get('page_num')) || 1; 
  
  // Increment the page number by 1
  pageNum += 1;
  
  // Update the 'page_num' parameter in the URL
  url.searchParams.set('page_num', pageNum);
  
  
  // Redirect to the updated URL with the new page number
  window.location.href = url.toString();
}



// for sidebar in mobile menu
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar_menu");
  sidebar.classList.toggle("open");
}


