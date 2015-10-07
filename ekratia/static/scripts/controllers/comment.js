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

    $scope.loadComments = function(thread_id){
        var data = Comment.query({id:thread_id}, function(){
            $scope.comments = data[0].children;
        });
    };

    $scope.delete = function(data) {
        data.children = [];
    };
    $scope.add = function(data) {

    };
    $scope.tree = [{name: "Comment ", nodes: []}];

}]);