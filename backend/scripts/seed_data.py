"""Seed Data Script for SHG Saathi Platform.

Populates realistic data across all 5 roles, orders, inventory, pricing,
allocations, production, quality, and payouts for demonstration and testing.
"""

import sys
import os
import json
from datetime import datetime, timezone, timedelta

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.session import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.user import User, SHG, SHGMember, Buyer, MemberCapacity
from app.models.order import Product, ProductSpecification, BulkOrder, OrderItem, OrderStatus
from app.models.work import WorkAllocation, ProductionRecord, ProductionBatch, AllocationStatus, BatchStatus
from app.models.quality import QualityInspection, QualityStatus
from app.models.pricing import PricingBreakdown
from app.models.inventory import Inventory, InventoryItemType, Supplier, MaterialPurchase, PurchaseStatus
from app.models.finance import MemberEarning, Payout, PayoutStatus, EarningPaymentStatus
from app.models.retail import RetailOrder, RetailOrderItem, RetailOrderStatus
from app.models.support import Document, DocumentType, OCRStatus, Notification


def seed():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).filter(User.email == "leader.radha@shgsaathi.in").first():
            print("Database already contains seed data. Skipping.")
            return

        print("Seeding Users & Roles...")
        # 1. SHG Leader
        leader = User(
            email="leader.radha@shgsaathi.in",
            hashed_password=hash_password("LeaderPass2026!"),
            full_name="Radha Devi",
            phone="+919845012345",
            role="SHG_LEADER",
            is_active=True
        )
        db.add(leader)
        db.flush()

        # 2. SHG Members (Women home-based artisans)
        member1_user = User(
            email="sita.embroidery@shgsaathi.in",
            hashed_password=hash_password("MemberPass2026!"),
            full_name="Sita Bai",
            phone="+919845023456",
            role="SHG_MEMBER",
            is_active=True
        )
        member2_user = User(
            email="geetha.weaver@shgsaathi.in",
            hashed_password=hash_password("MemberPass2026!"),
            full_name="Geetha Kumari",
            phone="+919845034567",
            role="SHG_MEMBER",
            is_active=True
        )
        member3_user = User(
            email="lakshmi.tailor@shgsaathi.in",
            hashed_password=hash_password("MemberPass2026!"),
            full_name="Lakshmi Gowda",
            phone="+919845045678",
            role="SHG_MEMBER",
            is_active=True
        )
        db.add_all([member1_user, member2_user, member3_user])
        db.flush()

        # 3. Buyer
        buyer_user = User(
            email="vikram.procurement@fabcraft.com",
            hashed_password=hash_password("BuyerPass2026!"),
            full_name="Vikram Mehta",
            phone="+919811055555",
            role="BUYER",
            is_active=True
        )
        db.add(buyer_user)
        db.flush()

        buyer_profile = Buyer(
            user_id=buyer_user.id,
            organization_name="FabCraft Retail Pvt Ltd",
            gst_number="29ABCDE1234F1Z5",
            contact_person="Vikram Mehta (Head Sourcing)",
            address="Brigade Road, Bengaluru, Karnataka",
            verified=True
        )
        db.add(buyer_profile)

        # 4. Federation Officer
        federation_officer = User(
            email="officer.ramesh@nrlm.gov.in",
            hashed_password=hash_password("OfficerPass2026!"),
            full_name="Ramesh Kumar KAS",
            phone="+919448011223",
            role="FEDERATION_OFFICER",
            is_active=True
        )
        db.add(federation_officer)

        # 5. Customer
        customer_user = User(
            email="priya.shoppe@gmail.com",
            hashed_password=hash_password("CustomerPass2026!"),
            full_name="Priya Sharma",
            phone="+919900112233",
            role="CUSTOMER",
            is_active=True
        )
        db.add(customer_user)
        db.flush()

        print("Seeding SHG & Member Profiles...")
        shg = SHG(
            name="Prerana Mahila Self-Help Group",
            registration_number="KA-MYS-NRLM-2023-091",
            address="Hunsur Taluk, Bilikere Village",
            district="Mysuru",
            state="Karnataka",
            bank_account_details="Canara Bank, Hunsur Branch, A/C: 110022334455, IFSC: CNRB0001234",
            leader_id=leader.id
        )
        db.add(shg)
        db.flush()

        # Member records and Capacities
        members_data = [
            (member1_user.id, ["embroidery", "kassuti_work"], 6.0, 100.0, "88776655441", "SBIN0001234"),
            (member2_user.id, ["weaving", "loom_stitching"], 5.0, 96.0, "88776655442", "SBIN0001234"),
            (member3_user.id, ["tailoring", "zipper_attachment"], 7.0, 98.5, "88776655443", "SBIN0001234")
        ]

        shg_members = []
        for uid, skills, hrs, hist_rate, acc, ifsc in members_data:
            m = SHGMember(
                user_id=uid,
                shg_id=shg.id,
                skills=json.dumps(skills),
                bank_account_number=acc,
                ifsc_code=ifsc,
                is_active=True
            )
            db.add(m)
            db.flush()
            shg_members.append(m)

            cap = MemberCapacity(
                member_id=m.id,
                product_specialization=skills[0],
                available_hours_per_day=hrs,
                current_workload=0.0,
                max_feasible_daily_quantity=12.0,
                historical_completion_rate=hist_rate,
                active_tasks_count=0
            )
            db.add(cap)

        print("Seeding Catalog Products & Specifications...")
        p1 = Product(
            name="Artisan Handloom Cotton Tote Bag",
            category="Bags & Accessories",
            description="100% organic cotton, handmade block printed festive tote bag with double stitched seams.",
            base_unit="piece",
            standard_rate=180.0,
            images=json.dumps(["/uploads/tote_front.jpg", "/uploads/tote_detail.jpg"]),
            is_active=True
        )
        p2 = Product(
            name="Handcrafted Brass Bell Wall Hanging",
            category="Home Decor",
            description="Traditional bell chime crafted with local bell-metal alloys.",
            base_unit="piece",
            standard_rate=350.0,
            is_active=True
        )
        db.add_all([p1, p2])
        db.flush()

        # Product specifications for inspection
        specs = [
            ProductSpecification(product_id=p1.id, parameter_name="Dimensions", target_value="38cm x 42cm", tolerance_range="+/- 1cm"),
            ProductSpecification(product_id=p1.id, parameter_name="Stitch Density", target_value="8 stitches/inch", tolerance_range="+/- 1"),
            ProductSpecification(product_id=p1.id, parameter_name="Handle Seam", target_value="Reinforced X-box stitch", tolerance_range="Exact")
        ]
        db.add_all(specs)

        print("Seeding Inventory & Suppliers...")
        supplier = Supplier(
            name="Mysuru Khadi & Cotton Weavers Cooperative",
            contact_person="Basavaraj Patil",
            phone="+919844001122",
            email="supplies@mysurukhadi.org",
            address="Industrial Suburb, Mysuru",
            materials_supplied=json.dumps(["raw cotton fabric", "dye colors", "zippers"]),
            reliability_score=98.0
        )
        db.add(supplier)
        db.flush()

        # Raw material inventory
        inv_fabric = Inventory(
            shg_id=shg.id,
            item_type=InventoryItemType.RAW_MATERIAL.value,
            item_name="Unbleached Organic Cotton Fabric (Meters)",
            unit="meter",
            physical_stock=350.0,
            bulk_reserved_stock=150.0,
            retail_reserved_stock=0.0,
            damaged_stock=0.0,
            unit_cost=75.0,
            low_stock_threshold=50.0
        )
        # Finished goods inventory
        inv_finished = Inventory(
            shg_id=shg.id,
            item_type=InventoryItemType.FINISHED_GOOD.value,
            item_name="Artisan Handloom Cotton Tote Bag",
            unit="piece",
            physical_stock=80.0,
            bulk_reserved_stock=50.0,
            retail_reserved_stock=10.0,
            damaged_stock=2.0,
            unit_cost=110.0,
            low_stock_threshold=15.0
        )
        db.add_all([inv_fabric, inv_finished])

        print("Seeding Bulk Orders, Pricing & Allocations...")
        order = BulkOrder(
            order_number="ORD-SHG-20261107-FAB01",
            buyer_id=buyer_profile.id,
            shg_id=shg.id,
            title="Corporate Diwali Gift Tote Bags",
            description="500 handcrafted bags for festive artisan gifting hampers",
            status=OrderStatus.IN_PRODUCTION.value,
            target_delivery_date=datetime.now(timezone.utc) + timedelta(days=20),
            total_order_value=90000.0,
            approved_price_per_unit=180.0,
            currency="INR",
            notes="Buyer requested block print on both sides."
        )
        db.add(order)
        db.flush()

        order_item = OrderItem(
            bulk_order_id=order.id,
            product_id=p1.id,
            quantity=500,
            unit_price=180.0,
            completed_quantity=180,
            pending_quantity=320,
            specifications="Block printed natural dye"
        )
        db.add(order_item)
        db.flush()

        # Approved Pricing Breakdown
        pricing = PricingBreakdown(
            bulk_order_id=order.id,
            total_material_cost=42000.0,
            labor_cost=25000.0,
            packaging_cost=3500.0,
            transportation_cost=4000.0,
            operational_expenses=2500.0,
            profit_margin_percentage=16.88,
            calculated_unit_price=154.0,
            suggested_selling_price=180.0,
            final_approved_price=180.0,
            is_approved=True,
            approved_by_id=leader.id,
            approved_at=datetime.now(timezone.utc) - timedelta(days=5),
            notes="Costing verified and approved with buyer."
        )
        db.add(pricing)

        # Work Allocations among the 3 members
        alloc1 = WorkAllocation(
            bulk_order_id=order.id,
            order_item_id=order_item.id,
            member_id=shg_members[0].id,
            allocated_quantity=170,
            completed_quantity=70,
            unit_rate=50.0,
            status=AllocationStatus.IN_PROGRESS.value,
            deadline=datetime.now(timezone.utc) + timedelta(days=15),
            ai_recommended=True
        )
        alloc2 = WorkAllocation(
            bulk_order_id=order.id,
            order_item_id=order_item.id,
            member_id=shg_members[1].id,
            allocated_quantity=160,
            completed_quantity=60,
            unit_rate=50.0,
            status=AllocationStatus.IN_PROGRESS.value,
            deadline=datetime.now(timezone.utc) + timedelta(days=15),
            ai_recommended=True
        )
        alloc3 = WorkAllocation(
            bulk_order_id=order.id,
            order_item_id=order_item.id,
            member_id=shg_members[2].id,
            allocated_quantity=170,
            completed_quantity=50,
            unit_rate=50.0,
            status=AllocationStatus.IN_PROGRESS.value,
            deadline=datetime.now(timezone.utc) + timedelta(days=15),
            ai_recommended=True
        )
        db.add_all([alloc1, alloc2, alloc3])
        db.flush()

        # Update member capacities with active workloads
        shg_members[0].capacity.current_workload = 100.0
        shg_members[0].capacity.active_tasks_count = 1
        shg_members[1].capacity.current_workload = 100.0
        shg_members[1].capacity.active_tasks_count = 1
        shg_members[2].capacity.current_workload = 120.0
        shg_members[2].capacity.active_tasks_count = 1

        print("Seeding Batches & Quality Inspections...")
        batch1 = ProductionBatch(
            bulk_order_id=order.id,
            work_allocation_id=alloc1.id,
            batch_number=f"BATCH-{order.id}-{alloc1.id}-001",
            quantity=35,
            status=BatchStatus.ACCEPTED.value,
            photo_urls=json.dumps(["/uploads/batch1_top.jpg", "/uploads/batch1_seam.jpg"])
        )
        db.add(batch1)
        db.flush()

        insp1 = QualityInspection(
            production_batch_id=batch1.id,
            status=QualityStatus.APPROVED.value,
            ai_score=92.5,
            ai_defects_detected=json.dumps([]),
            ai_explanation="Seams uniform, dimensions exact to spec.",
            ai_suggested_action="APPROVE",
            human_decision="APPROVED",
            human_reviewer_id=leader.id,
            reviewed_at=datetime.now(timezone.utc) - timedelta(days=1)
        )
        db.add(insp1)

        print("Seeding Earnings & Payout Records...")
        earning1 = MemberEarning(
            member_id=shg_members[0].id,
            bulk_order_id=order.id,
            work_allocation_id=alloc1.id,
            assigned_quantity=170,
            accepted_quantity=35,
            approved_rate=50.0,
            gross_earnings=1750.0,
            deductions=0.0,
            net_payable_amount=1750.0,
            payment_status=EarningPaymentStatus.CALCULATED.value
        )
        db.add(earning1)

        payout = Payout(
            shg_id=shg.id,
            payout_reference="PAY-SHG-1-202611-BATCH01",
            period_start=datetime.now(timezone.utc) - timedelta(days=30),
            period_end=datetime.now(timezone.utc),
            total_amount=1750.0,
            status=PayoutStatus.PENDING_GROUP_APPROVAL.value,
            notes="Fortnightly progress payout for accepted batch items."
        )
        db.add(payout)

        # Seed in-app notification
        notif = Notification(
            user_id=member1_user.id,
            title="Work Allocation Assigned",
            message="You have been allocated 170 units of Artisan Handloom Tote Bags for Order #1.",
            notification_type="WORK_ALLOCATION",
            reference_id=alloc1.id,
            reference_type="WorkAllocation",
            is_read=False
        )
        db.add(notif)

        db.commit()
        print("\nSeed Data Created Successfully!")
        print("----------------------------------------------------------------")
        print("Demo Credentials:")
        print("  SHG Leader:         leader.radha@shgsaathi.in         / LeaderPass2026!")
        print("  SHG Member 1:       sita.embroidery@shgsaathi.in      / MemberPass2026!")
        print("  SHG Member 2:       geetha.weaver@shgsaathi.in        / MemberPass2026!")
        print("  Buyer:              vikram.procurement@fabcraft.com   / BuyerPass2026!")
        print("  Federation Officer: officer.ramesh@nrlm.gov.in        / OfficerPass2026!")
        print("  Customer:           priya.shoppe@gmail.com            / CustomerPass2026!")
        print("----------------------------------------------------------------")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
