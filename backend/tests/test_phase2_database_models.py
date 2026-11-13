from datetime import date

from backend.app import create_app
from backend.config import TestingConfig
from backend.extensions import db
from backend.models import (
    ForecastDemand,
    Inventory,
    InventoryEvent,
    LeadTime,
    Location,
    MitigationOption,
    ProductionPlan,
    PurchaseOrder,
    Shortage,
    Sku,
    SkuSupplier,
    Supplier,
    SupplierCapacity,
)


def test_database_models_and_relationships_are_available():
    app = create_app(TestingConfig)

    with app.app_context():
        db.drop_all()
        db.create_all()

        location = Location(
            id="LOC-0001",
            code="WHS-001",
            name="Chicago Distribution Center",
            region="Midwest",
            country="USA",
            warehouse_type="DC",
            capacity_units=25000,
        )
        sku = Sku(
            id="SKU-000001",
            sku_code="SKU-000001",
            name="Premium Retail Box",
            category="Packaging",
            brand="NorthStar",
            unit_of_measure="EA",
        )
        supplier = Supplier(
            id="SUP-0001",
            supplier_code="SUP-0001",
            name="Alpha Components",
            supplier_type="External",
            country="USA",
            rating=4.7,
        )

        db.session.add_all([location, sku, supplier])
        db.session.commit()

        inventory = Inventory(
            id="INV-SKU-000001-LOC-0001",
            sku_id=sku.id,
            location_id=location.id,
            on_hand_quantity=150.0,
            reserved_quantity=15.0,
            safety_stock=30.0,
            reorder_point=50.0,
        )
        shortage = Shortage(
            id="SHORT-2026-000001",
            sku_id=sku.id,
            location_id=location.id,
            shortage_date=date(2026, 1, 10),
            projected_shortage_units=40.0,
            severity="high",
        )
        purchase_order = PurchaseOrder(
            id="PO-2026-000001",
            supplier_id=supplier.id,
            sku_id=sku.id,
            location_id=location.id,
            order_quantity=200.0,
            expected_delivery_date=date(2026, 1, 20),
            status="open",
        )
        forecast = ForecastDemand(
            id="DEM-SKU-000001-LOC-0001-2026W01",
            sku_id=sku.id,
            location_id=location.id,
            week_start=date(2026, 1, 5),
            forecast_units=180.0,
            lower_bound=150.0,
            upper_bound=210.0,
        )
        lead_time = LeadTime(
            id="LT-SUP-0001-SKU-000001-LOC-0001",
            supplier_id=supplier.id,
            sku_id=sku.id,
            location_id=location.id,
            lead_days=12,
            effective_from=date(2026, 1, 1),
        )
        capacity = SupplierCapacity(
            id="CAP-SUP-0001-SKU-000001",
            supplier_id=supplier.id,
            sku_id=sku.id,
            capacity_units=3000.0,
            effective_from=date(2026, 1, 1),
        )
        production_plan = ProductionPlan(
            id="PP-SKU-000001-2026W01",
            sku_id=sku.id,
            location_id=location.id,
            planned_quantity=350.0,
            start_date=date(2026, 1, 8),
            end_date=date(2026, 1, 15),
            status="planned",
        )
        inventory_event = InventoryEvent(
            id="INV-EVT-000001",
            inventory_id=inventory.id,
            event_type="stock_adjustment",
            quantity_delta=25.0,
            previous_quantity=125.0,
            new_quantity=150.0,
            reason="Cycle count correction",
        )
        mitigation = MitigationOption(
            id="MIT-SHORTAGE-ID-01",
            shortage_id=shortage.id,
            mitigation_type="expedite",
            action_description="Expedite inbound shipment from alternate supplier",
            recommended_quantity=80.0,
            cost_estimate=1500.0,
            impact_score=8.5,
        )
        sku_supplier = SkuSupplier(
            sku_id=sku.id,
            supplier_id=supplier.id,
            preferred_supplier=True,
            min_order_quantity=100.0,
            multi_source_approved=True,
        )

        db.session.add_all([
            inventory,
            shortage,
            purchase_order,
            forecast,
            lead_time,
            capacity,
            production_plan,
            inventory_event,
            mitigation,
            sku_supplier,
        ])
        db.session.commit()

        assert inventory.sku_id == sku.id
        assert forecast.location_id == location.id
        assert purchase_order.supplier_id == supplier.id
        assert shortage.mitigation_options[0].id == "MIT-SHORTAGE-ID-01"
        assert inventory.events[0].event_type == "stock_adjustment"
        assert len(db.metadata.tables) >= 12
        assert "created_at" in Sku.__table__.columns
        assert "updated_at" in Supplier.__table__.columns
        assert "effective_from" in LeadTime.__table__.columns
