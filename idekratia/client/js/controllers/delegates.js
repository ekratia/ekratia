'use strict';

var controllersModule = require('./_index');

/**
 * @ngInject
 */
function DelegatesCrtl($scope) {

  // ViewModel
  var vm = this;

  var user = {
  	delegates: [
	  	{fullname: 'Martin Luther King', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  	{fullname: 'Jhon Smith', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  	{fullname: 'Jhon Smith', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  	{fullname: 'Jhon Smith', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  	{fullname: 'Jhon Smith', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  	{fullname: 'Jhon Smith', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  ],
	  friends: [
	  	{fullname: 'Rocky Balboa', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  	{fullname: 'Jhon Smith', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  	{fullname: 'Jhon Smith', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  	{fullname: 'Jhon Smith', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  	{fullname: 'Jhon Smith', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  	{fullname: 'Jhon Smith', followers: 32, avatar: 'http://placehold.it/75x75/'},
	  ]
  };

  $scope.delegates = user.delegates;

  $scope.available_delegates = user.friends;

  $scope.undelegate = function (item) {
  	var idx = $scope.delegates.indexOf(item);
  	$scope.delegates.splice(idx,1);
  }

  $scope.addDelegate = function (item) {
  	$scope.delegates.push(item);

  	var idx = $scope.available_delegates.indexOf(item);
  	$scope.available_delegates.splice(idx,1);
  }


}

controllersModule.controller('DelegatesCrtl', DelegatesCrtl);