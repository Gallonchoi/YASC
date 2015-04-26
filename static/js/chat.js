(function() {
    // AngularJS APP Configuration
    var chatApp = angular.module('chatApp', ['luegg.directives']);

    chatApp
        .filter("timeHandler", function() {
            return function(time) {
                var now = new Date();
                time = parseInt((now.getTime() - time)/1000/60);
                if (time < 1)
                    time = "Just now";
                else
                    time += " mins ago";
                return time;
            };
        })
        .controller("MessageListCtrl", function($scope) {
            updater.start($scope);
            $scope.messages = [];
            $scope.sendMessage = function() {
                var msgNode = document.getElementById('compose-msg-input');
                var message = msgNode.value;
                if (message.length > 0) {
                    updater.sendMessage(message);
                    msgNode.value = '';
                }
            };
        });

    var updater = {
        connection: null,

        start: function($scope) {
            updater.connection = new WebSocket("ws://127.0.0.1:8888/message");
            updater.connection.onmessage = function(event) {
                var msg = JSON.parse(event.data);
                if (msg.type == "message") {
                    updater.showMessage($scope, msg);
                } else if(msg.type == "userlist") {
                    updater.updateUserList($scope, msg);
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
        },
        updateUserList: function($scope, userList) {
            $scope.$apply(function() {
                $scope.users = userList.users;
            });
        }
    };
}());
