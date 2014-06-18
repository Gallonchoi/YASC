// AngularJS APP Configuration
var chatApp = angular.module('chatApp', []);

chatApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('//');
    $interpolateProvider.endSymbol('//');
});

function MessageListCtrl($scope) {
    var connection = new WebSocket("ws://127.0.0.1:8888/message");
    connection.onmessage = function(event) {
        var message = jQuery.parseJSON(event.data);
        if (message.type == "message")
        {
            message.time = timeHandler(message.time);
            showMessage($scope, message);
        }
    };

    connection.onerror = function wsError(event) {
        console.log("Error: " + event.data);
    };

    $scope.messages = [];
    $scope.sendMessage = function() {
        var message = $("#message").val();
        if (message.length > 0)
        {
            connection.send(message);
            $("#message").val(null);
        }
    };
}

function timeHandler(time)
{
    var now = new Date();
    time = parseInt((now.getTime() - time)/1000/60);
    if (time < 1)
        time = "just now";
    else
        time += " mins ago";
    return time;
}

function showMessage($scope, message)
{
    // Force AngularJS binding the async data
    $scope.$apply(function() {
        $scope.messages.push(message);
    });
}
