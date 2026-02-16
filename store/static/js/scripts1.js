(async () => {
	await statsig.initialize(
		"client-Osdu8BmeT9x4jcQMDtf7SuU78BL1hrZm7Gt7tZE9x3g",
		{
			userID: 'some_user',
			ip: '112.12.13.123',
			custom: {
				new_user: true,
				level:2
			}
		}
	);
	// Page Visit Event Log
	statsig.logEvent(
		"page_view", 
		'Product Page', 
		{ 
			name: document.getElementById("product-title").innerHTML,
			prdcode: document.getElementById("prdcode").value	
		}
	);
	// Dynamic Config	
	const config = statsig.getConfig("first_config");
	if(config){
		let webprice = document.getElementById("proprice").value;
		webprice = parseFloat(webprice);
		
		console.log('webprice21: '+webprice);
		
		const price = config.get("price", webprice);
		const itemName = config.get("title", "What is Lorem Ipsum?");
		
		document.getElementById("product-title").innerHTML = itemName;	
		//document.getElementById("price").innerHTML = parseFloat(price);
		
		console.log('Sp Price: '+price);
		if(parseFloat(webprice) > parseFloat(price)){
			console.log('webprice: '+webprice);
			document.getElementById("sp-price").innerHTML = '$'+parseFloat(price);
			document.getElementById("proprice").value = parseFloat(price);
			document.getElementById("price").style.textDecoration = 'line-through';
		}
	}
	// Feature Gate
	let isUpdateUi = statsig.checkGate('pdp_ui');
	if(isUpdateUi){
		render(); 
	}
	// Experiment Code
	let bannerText = document.querySelector('#top-banner p').innerText;	
	const layer = statsig.getLayer("banner_ui");
	const newBannerText = layer.get("text", bannerText);	
	let textColor = layer.get("color", '#000');
	if(newBannerText){
		document.querySelector('#top-banner p').innerText = newBannerText;
	}
	if(textColor){
		document.querySelector('#top-banner p').style.color = textColor;
	} 
})();
/*
* Method for Event Log
*/
function addToCart(){
	//statsig.logEvent("add_to_cart", '1233456'); 
	statsig.logEvent(
		"add_to_cart", 
		document.getElementById("proprice").value, 
		{ 
			item_id: document.getElementById("prdcode").value, 
			quantity: document.getElementById("qty").value,
			user_segment: 'first_time_buyer',
		}
	); 
}
/*
* Method to change sections using Feature Gate
*/
function render(){
	var deliveryOptions = document.getElementById("delivery-options");
	console.log('deliveryOptions: '+deliveryOptions.innerHTML);
	var div = document.createElement("div");
	div.className = "col-md-3";	
	//div.style.background = "red";
	//div.style.color = "white";
	div.innerHTML = deliveryOptions.innerHTML;
	deliveryOptions.innerHTML = '';
	deliveryOptions.style.display = 'none';

	document.getElementById("pdp-main").prepend(div);
	
	var tabContent = [];
	for(let tabPane of document.getElementsByClassName('tab-pane')){
		tabContent.push(tabPane.innerHTML);
		//console.log('tabPane.innerHTML: '+tabPane.innerHTML);
	}
	
	
	var accordHTML = '<div class="accordion accordion-flush" id="accordionFlushExample">';
	
	
	
	
	var accButtons = [];
	var navButtons = document.getElementById("nav-tab").children;
	for(var i = 0; i < navButtons.length; i++) {
		//console.log('navButtons: '+navButtons[i].innerText);
		accButtons.push(navButtons[i].innerText);
		
		var accordItem = '<div class="accordion-item">';
			accordItem += '<h2 class="accordion-header" id="headingOne_'+i+'">';
			accordItem += '<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#list_'+i+'" aria-expanded="false" aria-controls="list_'+i+'">';
			accordItem += navButtons[i].innerText;
			accordItem += '</button>';
			accordItem += '</h2>';
			accordItem += '<div id="list_'+i+'" class="accordion-collapse collapse" aria-labelledby="list_'+i+'" data-bs-parent="#accordionFlushExample">';
				accordItem += '<div class="accordion-body">'+ tabContent[i] +'</div>';
			accordItem += '</div>';
		accordItem += '</div>';		
		
		
		accordHTML = accordHTML + accordItem;
	}
	accordHTML = accordHTML + '</div>';
	//console.log('accordHTML: '+accordHTML);
	
	document.getElementById('prod-details').innerHTML = accordHTML;
	
	/*for(let button of document.getElementsByClassName('button')){
		button.style.fontSize = '90px';
	}*/
	
	
	
}