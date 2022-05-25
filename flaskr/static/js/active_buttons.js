var activeRegions = new Set();

function addRegion(region) {
    activeRegions.add(region);
    // alert(Array.from(activeRegions).join(' '));
}

var btns = document.querySelectorAll(".btn");
Array.from(btns).forEach(item => {
  item.addEventListener("click", () => {
    if (item.className.includes('btn-success')){
        item.className = 'btn btn-outline-danger mr-sm-2 ';
    } else {
        item.className = 'btn btn-success mr-sm-2 ';
    }
});
});