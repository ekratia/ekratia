'use strict';

/**
 * @ngdoc function
 * @name frontApp.controller:CommentsController
 * @description
 * # CommentsController
 * Controller of the application
 * Handles information from the API to be connected with the view
 */
angular.module('Ekratia')
  .controller('CommentsController',
    ['$scope', 'Comment',  '$location','$anchorScroll', 'VoteComment',
    function ($scope, Comment, $location, $anchorScroll, VoteComment) {
    $scope.thread_id = null;
    $scope.anchor = null;

    $scope.loadComments = function(thread_id, anchor){
        $scope.thread_id = thread_id;
        var data = Comment.query({id:thread_id}, function(){
            $scope.comments = data;
        });
        if(anchor === true){
            if($location.hash()){
                $scope.anchor = $location.hash();
            }
        }
    };

    $scope.delete = function(data) {
        data.children = [];
    };
    $scope.add = function(data) {

    };
    $scope.tree = [{name: "Comment ", nodes: []}];

    $scope.saveComment = function(comment){
        $scope.anchor = null;
        var data = {content:comment.reply, parent:comment.id}
        Comment.save({id:$scope.thread_id},data, function(data){
            $scope.loadComments($scope.thread_id, false);
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

    $scope.goTo = function(id) {
      $location.hash(id);
      $anchorScroll();
    };

    $scope.$on('onRepeatLast', function(scope, element, attrs){
        if($scope.anchor){
            $scope.goTo($scope.anchor);
        }
    });

    $scope.commentVote = function(comment, vote){
        $scope.anchor = null;
        VoteComment.save({comment:comment.id, value:vote}, function(data){
            $scope.loadComments($scope.thread_id, false);
        }, function(){
            console.log('failed');
        });
    };
    $scope.commentVoteClass = function(comment, selector){
        if(selector == 'up'){
            if(comment.data.current_user_vote >0){
                return 'active';  
            }
        }
        if(selector == 'down'){
            if(comment.data.current_user_vote <0){
                return 'active';  
            }
        }
        return 'inactive';
    };
}]);