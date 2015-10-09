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
    ['$scope', 'Comment', '$location','$anchorScroll',
    function ($scope, Comment, $location, $anchorScroll) {
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
    };

    $scope.toggl_children = function(comment){
        comment.close_children = !comment.close_children;
    };

    $scope.close_children = function(comment){
        if(!comment.close_children && comment.children){
            return true;
        }else{
            return false;
        }
    }
    $scope.goTop = function(id) {
      $location.hash('top');
      $anchorScroll();
    }
    $scope.goBottom = function(id) {
      $location.hash('bottom');
      $anchorScroll();
    }
    $scope.goTo = function(id) {
      $location.hash(id);
      $anchorScroll();
    };

    $scope.$on('onRepeatLast', function(scope, element, attrs){
        if($location.hash()){
            $scope.goTo(String($location.hash()));
        }
    });

}]);