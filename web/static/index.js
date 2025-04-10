function change_modal(event){
    const parentDiv = event.target.closest("div"); // get the parent element
    const grandparentDiv = parentDiv ? parentDiv.parentElement : null; // get the grand parent element

    if(grandparentDiv){
        // console.log(grandparentDiv.className);  // console log the classname there for test
        const show_modal = document.getElementsByClassName(event.target.id);

        grandparentDiv.style.display = "none";
        for (let i=0; i < show_modal.length; i++){
            show_modal[i].style.display = "block";
            // show_modal[i].pointerEvents = "auto"; // Enable interaction
        }
    }
    else{
        alert("Code Error!")
    }
}