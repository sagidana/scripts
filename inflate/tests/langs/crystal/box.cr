class Box
  def initialize
    @size = 1
  end

  def helper(value)
    value + @size
  end

  def greet(value)
    helper(value) * 2
  end

  def runner
    greet(3)
  end
end
