function change_modal(event) {
    const parentDiv = event.target.closest("div"); // get the parent element
    const grandparentDiv = parentDiv ? parentDiv.parentElement : null; // get the grand parent element

    if (grandparentDiv) {
        // console.log(grandparentDiv.className);  // console log the classname there for test
        const show_modal = document.getElementsByClassName(event.target.id);

        grandparentDiv.style.display = "none";
        for (let i = 0; i < show_modal.length; i++) {
            show_modal[i].style.display = "block";
            // show_modal[i].pointerEvents = "auto"; // Enable interaction
        }
    }
    else {
        alert("Code Error!")
    }
}

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