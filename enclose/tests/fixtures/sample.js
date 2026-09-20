function helper(value) {
  return value + 1;
}

const grow = (size) => {
  return helper(size);
};

class Widget {
  constructor(size) {
    this.size = size;
  }

  grow() {
    this.size = grow(this.size);
    return this.size;
  }
}

function useWidget() {
  const widget = new Widget(3);
  [1, 2].forEach(function (n) {
    widget.grow();
  });
  return widget.size;
}
