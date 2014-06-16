var chatApp = angular.module('chatApp', []);

chatApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('//');
    $interpolateProvider.endSymbol('//');
});


chatApp.controller('DemoController', function DemoController() {
    this.label = "This bindings is brought you you by // interpolation symbols.";
});

function MessageListCtrl($scope) {
    var connection = new WebSocket("ws://127.0.0.1:8888/message");
    connection.onmessage = function(event) {
        var obj = jQuery.parseJSON(event.data);
        if (obj.type == "message")
        {
            $scope.messages.push(obj);
        }
        else if (obj.type == "info")
        {

        }
    };
    connection.onerror = function wsError(event) {
        console.log("Error: " + event.data);
    };
    $scope.messages = [];
    $scope.sendMessage = function() {
        var message = $("#message").val();
        connection.send(message);
        $("#message").val(null);
    };
}
