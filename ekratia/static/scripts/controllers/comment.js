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
    $scope.thread_id = null;

    $scope.loadComments = function(thread_id){
        $scope.thread_id = thread_id;
        var data = Comment.query({id:thread_id}, function(){
            $scope.comments = data;
        });
    };

    $scope.delete = function(data) {
        data.children = [];
    };
    $scope.add = function(data) {

    };
    $scope.tree = [{name: "Comment ", nodes: []}];

    $scope.saveComment = function(comment){
        console.log(comment);
        var data = {content:comment.reply, parent:comment.id}
        Comment.save({id:$scope.thread_id},data, function(data){
            $scope.loadComments($scope.thread_id);
        });
        
    }
    $scope.toggleCommentForm = function(comment){
        comment.open_form = !comment.open_form;
    }

}]);