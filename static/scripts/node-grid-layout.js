function resizeUsernameNodes() {
    const usernameList = document.querySelector(".username-list"); // get the list
    const nodes = usernameList.querySelectorAll(".username-node"); // get the nodes
    if (nodes.length === 0) return; // no nodes, do nothing
    const parentRect = usernameList.getBoundingClientRect(); // get parent dimensions
    const parentWidth = parentRect.width;
    const parentHeight = parentRect.height;
    const numNodes = nodes.length; // node count
    const gridSize = Math.ceil(Math.sqrt(numNodes)); // calculate grid size
    const diameter = Math.min(parentWidth / gridSize, parentHeight / gridSize); // calculate diameter of each node
    usernameList.style.display = "grid"; // set list as grid
    usernameList.style.gridTemplateColumns = `repeat(${gridSize}, 1fr)`; // establish grid columns
    usernameList.style.gridTemplateRows = `repeat(${Math.ceil(numNodes / gridSize)}, 1fr)`; // establish grid rows
    usernameList.style.placeItems = "center"; // center nodes horizontally and vertically
    nodes.forEach(node => { // position each node
      node.style.width = `${diameter}px`;
      node.style.height = `${diameter}px`;
      node.style.borderRadius = "50%"; // make each node round
    });
  }

  document.addEventListener("DOMContentLoaded", resizeUsernameNodes);
  document.body.addEventListener("htmx:afterSwap", resizeUsernameNodes);
  window.addEventListener("resize", resizeUsernameNodes);