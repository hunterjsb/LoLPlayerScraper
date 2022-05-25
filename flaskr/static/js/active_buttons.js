var activeRegions = new Set();

function addRegion(region) {
    activeRegions.add(region)
    ARSet = Array.from(activeRegions).join(' ')
    alert(ARSet);
}