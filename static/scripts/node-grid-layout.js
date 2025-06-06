function handleNodeClick(event) { // click event handler for username nodes
  const node = event.target.closest('.username-node'); // find the nearest element from the clicked element
  if (node && usernameList.contains(node)) { // check if a valid element was found
    window.open(`https://x.com/${node.innerHTML}`, "_blank");
    usernameList.removeChild(node); // remove element
    resizeUsernameNodes(); // update grid layout
  }
}

function handleButtonClick(_) { // click event handler for tab buttons
  resizeUsernameNodes();
}

function resizeUsernameNodes() {
  const usernameList = document.querySelector(".username-list"); // get the list

  const followingNotFollowersButton = document.getElementById("tab1");
  const followersNotFollowingButton = document.getElementById("tab2");

  if (!followingNotFollowersButton || !followersNotFollowingButton) {
    console.warn('Tab buttons not found');
    return;
  }

  followersNotFollowingButton.addEventListener("click", handleButtonClick);
  followingNotFollowersButton.addEventListener("click", handleButtonClick);

  const isFollowersNotFollowingButtonChecked = followersNotFollowingButton.checked; // determine whether or not the buttons have been clicked
  const isFollowingNotFollowersButtonChecked = followingNotFollowersButton.checked;
  const followersNotFollowingNodes = usernameList.getElementsByClassName("followerNotFollowing"); // get each relationship list
  const followingNotFollowersNodes = usernameList.getElementsByClassName("followingNotFollower");

  const nodes = usernameList.querySelectorAll(".username-node"); // get the nodes
  if (nodes.length === 0) return; // no nodes, do nothing
  var numNodes = nodes.length; // node count

  var nodeDisplayed = false;
  Array.from(followersNotFollowingNodes).forEach(node => { // hide/show usernames based on button checked
    if (!isFollowersNotFollowingButtonChecked) {
      node.style.display = "none";
      numNodes -= 1;
    }
    else {
      node.style.display = "block";
      nodeDisplayed = true;
    }
  });

  Array.from(followingNotFollowersNodes).forEach(node => { // hide/show usernames based on button checked
    if (!isFollowingNotFollowersButtonChecked) {
      node.style.display = "none";
      numNodes -= 1;
    }
    else {
      node.style.display = "block";
      nodeDisplayed = true;
    }
  })
  const instructionsLabel = document.getElementById("instructions");
  if (nodeDisplayed)
  {
    instructionsLabel.style.display = "none";
  }
  else
  {
    instructionsLabel.style.display = "block";
  }
  const parentRect = usernameList.getBoundingClientRect(); // get parent dimensions
  const parentLength = Math.min(parentRect.width, parentRect.height);

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

  nodes.forEach(node => { // for each node
    node.removeEventListener('click', handleNodeClick); // remove the click handler
    node.addEventListener('click', handleNodeClick); // add the click handler
  })
}

document.addEventListener("DOMContentLoaded", resizeUsernameNodes);
document.body.addEventListener("htmx:afterSwap", resizeUsernameNodes);
window.addEventListener("resize", resizeUsernameNodes);