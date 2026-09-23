.class public Lsample/Box;
.super Ljava/lang/Object;

.method public helper(I)I
    .locals 1
    add-int/lit8 v0, p1, 0x1
    return v0
.end method

.method public greet(I)I
    .locals 1
    invoke-virtual {p0, p1}, Lsample/Box;->helper(I)I
    move-result v0
    return v0
.end method

.method public runner()I
    .locals 1
    invoke-virtual {p0}, Lsample/Box;->greet(I)I
    move-result v0
    return v0
.end method
