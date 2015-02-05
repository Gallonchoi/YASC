// AngularJS APP Configuration
var chatApp = angular.module('chatApp', []);

function MessageListCtrl($scope, $location, $anchorScroll) {
    updater.start($scope, $location, $anchorScroll);
    $scope.messages = [];
    $scope.sendMessage = function() {
        var msg_node = document.getElementById('message');
        var message = msg_node.value;
        if (message.length > 0) {
            updater.sendMessage(message);
            msg_node.value = '';
        }
    };
}

chatApp.filter("timeHandler", function() {
    return function(time) {
        var now = new Date();
        time = parseInt((now.getTime() - time)/1000/60);
        if (time < 1)
            time = "Just now";
        else
            time += " mins ago";
        return time;
    };
});

var updater = {
    connection: null,

    start: function($scope, $location, $anchorScroll) {
        updater.connection = new WebSocket("ws://127.0.0.1:8888/message");
        updater.connection.onmessage = function(event) {
            var msg = JSON.parse(event.data);
            if (msg.type == "message") {
                updater.showMessage($scope, msg);
                $location.hash('bottom');
                $anchorScroll();
            }
        };
        updater.connection.onerror = function wsError(event) {
            console.log("Error: " + event.data);
        };
    },

    sendMessage: function(message) {
        updater.connection.send(message);
    },

    showMessage: function($scope, message) {
        // Force AngularJS binding the async data
        $scope.$apply(function() {
            $scope.messages.push(message);
        });
    }
};
