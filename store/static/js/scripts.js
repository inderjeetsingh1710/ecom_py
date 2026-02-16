$(document).ready(function(){

	let moves = ["✊", "🖐", "✌"];	
	
	$("#setuser").click(function(){
		let userID = $('#user_id').val();
		if(userID == ''){
			alert("Please enter User Id First");
			return false;
		}
		$('#user-section').hide();
		console.log('userID: '+userID);
		
		(async () => {
		  await statsig.initialize(
			"client-Osdu8BmeT9x4jcQMDtf7SuU78BL1hrZm7Gt7tZE9x3g",
			{
			  userID: userID,
			}
		  );
		  const layer = statsig.getLayer("rps_experiment");
		  moves = layer.get("moves", moves);

		  const actions = document.getElementById("actions");

		  // Dynamically add buttons to DOM
		  moves.forEach((val, index) => {
			const button = document.createElement("button");
			button.textContent = val;
			button.onclick = () => onPick(index);
			button.className = "button btn btn-info";
			actions.appendChild(button);
		  });
		  
		  let showLargerText = statsig.checkGate('larger_button_text');
		  if(showLargerText){
			 render(); 
		  }	  
		  
		})();
		
	});	
	
	function onPick(playerIndex) {
		const randomMove = moves[Math.floor(Math.random() * moves.length)];

		const cpuIndex = moves.indexOf(randomMove);
		const loseIndex = (playerIndex + 1) % moves.length;

		let result = "Won";
		if (cpuIndex === playerIndex) {
			result = "Tied";
		} else if (cpuIndex === loseIndex) {
			result = "Lost";
		}
		document.getElementById("computer-move-text").innerHTML =  "Computer picked " + randomMove;
		document.getElementById("result-text").innerHTML = "You " + result;
		statsig.logEvent("game_played", result.toLowerCase()); // new line
	}
	
	$(".onPick").click(function(){
		let playerIndex = $(this).data("index");
		console.log('playerIndex: '+playerIndex);
		const randomMove = moves[Math.floor(Math.random() * moves.length)];

		const cpuIndex = moves.indexOf(randomMove);
		const loseIndex = (playerIndex + 1) % moves.length;

		let result = "Won";
		if (cpuIndex === playerIndex) {
			result = "Tied";
		} else if (cpuIndex === loseIndex) {
			result = "Lost";
		}
		document.getElementById("computer-move-text").innerHTML =  "Computer picked " + randomMove;
		document.getElementById("result-text").innerHTML = "You " + result;
		statsig.logEvent("game_played", result.toLowerCase()); // new line	
		
	});
	
	function render(){
		for(let button of document.getElementsByClassName('button')){
			button.style.fontSize = '90px';
		}
	}

});

/*let moves = ["✊", "🖐", "✌"];
(async () => {
  await statsig.initialize(
	"client-Osdu8BmeT9x4jcQMDtf7SuU78BL1hrZm7Gt7tZE9x3g",
	{
	  userID: 'some_user',
	}
  );
  
  const layer = statsig.getLayer("rps_experiment");
  moves = layer.get("moves", moves);

  const actions = document.getElementById("actions");

  // Dynamically add buttons to DOM
  moves.forEach((val, index) => {
    const button = document.createElement("button");
    button.textContent = val;
    button.onclick = () => onPick(index);
    button.className = "button btn btn-info";
    actions.appendChild(button);
  });
  
  let showLargerText = statsig.checkGate('larger_button_text');
  if(showLargerText){
	 render(); 
  }
  
})();

function onPick(playerIndex) {
	const randomMove = moves[Math.floor(Math.random() * moves.length)];

	const cpuIndex = moves.indexOf(randomMove);
	const loseIndex = (playerIndex + 1) % moves.length;

	let result = "Won";
	if (cpuIndex === playerIndex) {
		result = "Tied";
	} else if (cpuIndex === loseIndex) {
		result = "Lost";
	}
	document.getElementById("computer-move-text").innerHTML =  "Computer picked " + randomMove;
	document.getElementById("result-text").innerHTML = "You " + result;
	statsig.logEvent("game_played", result.toLowerCase()); // new line
}

function render(){
	for(let button of document.getElementsByClassName('button')){
		button.style.fontSize = '90px';
	}
}*/