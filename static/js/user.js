var user = user || {
    Collection: {},
    Model: {},
    View: {}
}
user.Collection = Backbone.Collection.extend({
    model: user.Model
});
user.Model = Backbone.Model.extend({
    initialize: function() {
    }
});
user.View = Backbone.View.extend({
    tagName: "div",
    className: "user-root",
    initialize: function() {
    },
    render: function() {
    }
});