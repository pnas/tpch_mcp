from . import db

class Region(db.Model):
    r_regionkey = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String(25), nullable=False)
    r_comment = db.Column(db.String(152))

class Nation(db.Model):
    n_nationkey = db.Column(db.Integer, primary_key=True)
    n_name = db.Column(db.String(25), nullable=False)
    n_regionkey = db.Column(db.Integer, db.ForeignKey('region.r_regionkey'), nullable=False)
    n_comment = db.Column(db.String(152))

class Part(db.Model):
    p_partkey = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(55), nullable=False)
    p_mfgr = db.Column(db.String(25), nullable=False)
    p_brand = db.Column(db.String(10), nullable=False)
    p_type = db.Column(db.String(25), nullable=False)
    p_size = db.Column(db.Integer, nullable=False)
    p_container = db.Column(db.String(10), nullable=False)
    p_retailprice = db.Column(db.Numeric, nullable=False)
    p_comment = db.Column(db.String(23), nullable=False)

class Supplier(db.Model):
    s_suppkey = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(25), nullable=False)
    s_address = db.Column(db.String(40), nullable=False)
    s_nationkey = db.Column(db.Integer, db.ForeignKey('nation.n_nationkey'), nullable=False)
    s_phone = db.Column(db.String(15), nullable=False)
    s_acctbal = db.Column(db.Numeric, nullable=False)
    s_comment = db.Column(db.String(101), nullable=False)

class Partsupp(db.Model):
    ps_partkey = db.Column(db.Integer, db.ForeignKey('part.p_partkey'), primary_key=True)
    ps_suppkey = db.Column(db.Integer, db.ForeignKey('supplier.s_suppkey'), primary_key=True)
    ps_availqty = db.Column(db.Integer, nullable=False)
    ps_supplycost = db.Column(db.Numeric, nullable=False)
    ps_comment = db.Column(db.String(199), nullable=False)

class Customer(db.Model):
    c_custkey = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(25), nullable=False)
    c_address = db.Column(db.String(40), nullable=False)
    c_nationkey = db.Column(db.Integer, db.ForeignKey('nation.n_nationkey'), nullable=False)
    c_phone = db.Column(db.String(15), nullable=False)
    c_acctbal = db.Column(db.Numeric, nullable=False)
    c_mktsegment = db.Column(db.String(10), nullable=False)
    c_comment = db.Column(db.String(117), nullable=False)

class Orders(db.Model):
    o_orderkey = db.Column(db.Integer, primary_key=True)
    o_custkey = db.Column(db.Integer, db.ForeignKey('customer.c_custkey'), nullable=False)
    o_orderstatus = db.Column(db.String(1), nullable=False)
    o_totalprice = db.Column(db.Numeric, nullable=False)
    o_orderdate = db.Column(db.Date, nullable=False)
    o_orderpriority = db.Column(db.String(15), nullable=False)
    o_clerk = db.Column(db.String(15), nullable=False)
    o_shippriority = db.Column(db.Integer, nullable=False)
    o_comment = db.Column(db.String(79), nullable=False)

class Lineitem(db.Model):
    l_orderkey = db.Column(db.Integer, db.ForeignKey('orders.o_orderkey'), primary_key=True)
    l_partkey = db.Column(db.Integer, primary_key=True)
    l_suppkey = db.Column(db.Integer, primary_key=True)
    l_linenumber = db.Column(db.Integer, primary_key=True)
    l_quantity = db.Column(db.Numeric, nullable=False)
    l_extendedprice = db.Column(db.Numeric, nullable=False)
    l_discount = db.Column(db.Numeric, nullable=False)
    l_tax = db.Column(db.Numeric, nullable=False)
    l_returnflag = db.Column(db.String(1), nullable=False)
    l_linestatus = db.Column(db.String(1), nullable=False)
    l_shipdate = db.Column(db.Date, nullable=False)
    l_commitdate = db.Column(db.Date, nullable=False)
    l_receiptdate = db.Column(db.Date, nullable=False)
    l_shipinstruct = db.Column(db.String(25), nullable=False)
    l_shipmode = db.Column(db.String(10), nullable=False)
    l_comment = db.Column(db.String(44), nullable=False)
    __table_args__ = (db.ForeignKeyConstraint([l_partkey, l_suppkey], [Partsupp.ps_partkey, Partsupp.ps_suppkey]), {})
