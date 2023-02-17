chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.action == "getText") {
      let text = window.getSelection().toString();
      sendResponse({data: text});
    }
});

// HTML SENDING PART
chrome.runtime.onInstalled.addListener(function() {
  chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules([{
      conditions: [new chrome.declarativeContent.PageStateMatcher({
        pageUrl: {hostEquals: 'developer.chrome.com'},
      })
      ],
          actions: [new chrome.declarativeContent.ShowPageAction()]
    }]);
  });
});


