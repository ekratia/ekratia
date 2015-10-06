'use strict';

/**
 * @ngdoc function
 * @name frontApp.controller:MainController
 * @description
 * # MainController
 * Controller of the application
 * Handles information from the API to be connected with the view
 */
angular.module('Ekratia')
  .controller('CommentsController',
    ['$scope', 'Comment',
    function ($scope, Comment) {
        $scope.comments = [
        {"id":1,"content":"comment 1","date":"2015-10-06T03:11:02.458273Z","depth":0,"thread":1,"parent":null,"user":1},
        {"id":2,"content":"comment 2","date":"2015-10-06T03:11:02.458273Z","depth":0,"thread":1,"parent":1,"user":1},
        {"id":3,"content":"comment 3","date":"2015-10-06T03:11:02.458273Z","depth":0,"thread":1,"parent":2,"user":1}
        ];

    $scope.delete = function(data) {
        data.nodes = [];
    };
    $scope.add = function(data) {
        var post = data.nodes.length + 1;
        var newName = data.name + '-' + post;
        data.nodes.push({name: newName,nodes: []});
    };
    $scope.tree = [{name: "Comment ", nodes: []}];

}]);