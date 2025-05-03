function resizeUsernameNodes() {
    const usernameList = document.querySelector(".username-list"); // get the list
    const nodes = usernameList.querySelectorAll(".username-node"); // get the nodes
    if (nodes.length === 0) return; // no nodes, do nothing
    const parentRect = usernameList.getBoundingClientRect(); // get parent dimensions
    const parentLength = Math.min(parentRect.width, parentRect.height);
    const numNodes = nodes.length; // node count
    const gridSize = Math.min(4, Math.ceil(Math.sqrt(numNodes))); // calculate grid size with a limit
    if (numNodes > 16) // add scroll bar if exceeds 16 nodes
    {
      usernameList.style.overflowY = "auto";
      usernameList.style.overflowX = "hidden";
    }
    const diameter = Math.min(parentLength / gridSize, parentLength / gridSize) * 0.96; // calculate diameter of each node
    usernameList.style.display = "grid"; // set list as grid
    usernameList.style.gridTemplateColumns = `repeat(${gridSize}, 1fr)`; // establish grid columns
    usernameList.style.gridTemplateRows = `repeat(${Math.ceil(numNodes / gridSize)}, 1fr)`; // establish grid rows
    usernameList.style.placeItems = "center"; // center nodes horizontally and vertically
    nodes.forEach(node => { // position each node
      node.style.width = `${diameter}px`;
      node.style.height = `${diameter}px`;
      node.style.borderRadius = "50%"; // make each node round
    });

    function handleNodeClick(event) { // click event handler for username nodes
      const node = event.target.closest('.username-node'); // find the nearest element from the clicked element
      if (node && usernameList.contains(node)) { // check if a valid element was found
        window.open(`https://x.com/${node.innerHTML}`, "_blank");
          usernameList.removeChild(node); // remove element
          resizeUsernameNodes(); // update grid layout
      }
  }

    nodes.forEach(node => { // for each node
      node.removeEventListener('click', handleNodeClick); // remove the click handler
      node.addEventListener('click', handleNodeClick); // add the click handler
    })
  }

  document.addEventListener("DOMContentLoaded", resizeUsernameNodes);
  document.body.addEventListener("htmx:afterSwap", resizeUsernameNodes);
  window.addEventListener("resize", resizeUsernameNodes);