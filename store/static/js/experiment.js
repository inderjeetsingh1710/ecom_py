// Trick to launch the code, no matter at which loading state it was loaded to a page.
  (function () {
    if (
      document.readyState === "interactive" ||
      document.readyState === "complete"
    ) {
      StartExperiment(); // Change function name there as well
    } else {
      document.addEventListener("DOMContentLoaded", StartExperiment); // Change function name there as well
    }
  })();
  
  
  function StartExperiment(){
	var previewMode = false;
    var version = 0;
    var experimentOptions = {
      testName: "saba007", // Same name as in the Statsig.
      testSelector: 'addtocart', // XPATH selector, will be checked by statsig init container.
      launchExperiment: launchTest, // Function to launch the test, will be called with value provided by statsig.
    };

	var urlParams = new URLSearchParams(window.location.search);
    if (
      urlParams.get("ex") === experimentOptions.testName ||
      localStorage.getItem(experimentOptions.testName)
    ) {
      previewMode = true;
      version =
        urlParams.get("v") ||
        localStorage.getItem(experimentOptions.testName) ||
        0;
      localStorage.setItem(experimentOptions.testName, version);
    } else if (localStorage.getItem(experimentOptions.testName)) {
      version = localStorage.getItem(experimentOptions.testName);
    }
	
	console.log('previewMode: '+previewMode);
	console.log('version: '+version);
	
	if (previewMode) {
		console.log('In previewMode');  
      if (document.querySelector(experimentOptions.testSelector))
        experimentOptions.launchExperiment(version);
    } else {
      if (window.statsigReady) {
		console.log('statsigReady');  
        window.statsigRunExperiment(experimentOptions);
      } else {
		console.log('statsig Not Ready');    
        if (!window.statsigExperiments) {
          window.statsigExperiments = [];
        }
        window.statsigExperiments.push(experimentOptions);
      }
    }
	
	function launchTest(version) {
		console.log('launchTest version: '+version);
		if(version == 0) return;      
    }  
	  
  }