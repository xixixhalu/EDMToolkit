
var Class2 = {};

Class2.name = "Class2";              // Model name

Class2.attributes = [            // Model attribute list
    "class2Attribute2" ,
"class2Attribute1" 
];

// Model functions

Class2.createClass2 = function(data, success, error) {
    // Wrap data

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.createOne(Class2.name, data, successCB, errorCB);
};

Class2.readClass2 = function(data, success, error) {
    // Wrap data

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.readOne(Class2.name, data, successCB, errorCB);
};

Class2.updateClass2 = function(search, update, success, error) {
    // Wrap data
    var data = {
        oldData : search,
        newData : update
    };

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.update(Class2.name, data, successCB, errorCB);
};

Class2.deleteClass2 = function(data, success, error) {
    // Wrap data

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.delete(Class2.name, data, successCB, errorCB);
};

Class2.get = function(id, success, error) {
    // Wrap data
    var data = {"_id" : id};

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.readOne(Class2.name, data, successCB, errorCB);
};

Class2.set = function(id, newData, success, error) {
    // Wrap data
    var data = {"_id" : id, "newData" : newData};

    // Define callback function
    function successCB(msg) {
        // Success handling
        success(msg);
    }

    function errorCB(msg) {
        // Error handling
        error(msg);
    }

    DBAdapter.update(Class2.name, data, successCB, errorCB);
};

// Add the other functions here

Class2.op1 = function( ) {
    // Define data operation logic

    // Wrap data

    // Define callback function
    function successCB(msg) {
        // Success handling
    }

    function errorCB(msg) {
        // Error handling
    }

    // Call RESTful API via DBAdapter

};

Class2.op2 = function( ) {
    // Define data operation logic

    // Wrap data

    // Define callback function
    function successCB(msg) {
        // Success handling
    }

    function errorCB(msg) {
        // Error handling
    }

    // Call RESTful API via DBAdapter

};


