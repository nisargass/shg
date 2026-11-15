"""Seed Full Demo Script for SHG Saathi Platform.

Populates complete realistic demo data for Pragati Mahila Sangha, EcoFab,
KSRLPS NRLM Federation, all 4 portals, and real database relationships.
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
from app.models.logistics import LogisticsRecord, Shipment
from app.models.support import Document, DocumentType, OCRStatus, Notification, AIAnalysisRecord


def seed_full_demo():
    print("Ensuring database tables exist...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if Pragati SHG already seeded
        existing_shg = db.query(SHG).filter(SHG.name == "Pragati Mahila Sangha").first()
        if existing_shg:
            print("Pragati Mahila Sangha demo data already seeded. Skipping duplicate seeding.")
            return

        print("Seeding Users & Roles for Pragati SHG Ecosystem...")

        # Default password for demo personas
        default_pw = hash_password("Saathi@2026")

        # 1. SHG Leader: Savitribai Shinde
        leader = User(
            email="savitribai@pragati-shg.org",
            hashed_password=default_pw,
            full_name="Savitribai Shinde",
            phone="+91 98452 11045",
            role="SHG_LEADER",
            is_active=True
        )
        db.add(leader)
        db.flush()

        # 2. SHG Members
        members_spec = [
            ("sunita.rathod@shg.in", "Sunita Rathod", "+91 97412 88390", ["Heavy Fabric Stitching", "Bag Handle Attachment", "Zipper Fixing"], 5.0, 96.0, "Expert (Tier 1)", 3.2, 180, "Channapatna", "SBIN0040192 (A/C ...4821)"),
            ("radhabai.hiremath@shg.in", "Radhabai Hiremath", "+91 98450 71123", ["Fabric Cutting", "Pattern Stenciling"], 6.0, 92.0, "Advanced", 5.0, 220, "Ijoor", "KARB0000122 (A/C ...9102)"),
            ("lakshmi.devamma@shg.in", "Lakshmi Devamma", "+91 94812 55210", ["Precision Stitching", "Quality Inspection"], 4.5, 98.0, "Master Craftsman", 2.8, 150, "Kailancha", "CNRB0001882 (A/C ...3319)"),
            ("meenakshi.k@shg.in", "Meenakshi Kulkarni", "+91 99014 38291", ["Zipper Attachment", "Lining Stitching"], 4.0, 88.0, "Intermediate", 2.2, 120, "Bidadi", "BARB0CHANN (A/C ...5501)"),
            ("anusuya.bai@shg.in", "Anusuya Bai", "+91 96112 04821", ["Embroidery", "Screen Printing Finishing"], 5.0, 94.0, "Advanced", 2.5, 140, "Channapatna", "SBIN0040192 (A/C ...1190)"),
            ("parvati.gowda@shg.in", "Parvati Gowda", "+91 98801 77294", ["Ironing & Packaging", "Label Tagging"], 6.0, 95.0, "Standard", 7.5, 250, "Ijoor", "PKGB0012093 (A/C ...7712)")
        ]

        shg_member_users = []
        for email, name, phone, skills, hrs, on_time, level, speed, workload, village, acct in members_spec:
            u = User(
                email=email,
                hashed_password=default_pw,
                full_name=name,
                phone=phone,
                role="SHG_MEMBER",
                is_active=True
            )
            db.add(u)
            shg_member_users.append((u, skills, hrs, on_time, level, speed, workload, village, acct))
        db.flush()

        # 3. Buyer: Arvind Deshmukh (EcoFab Bangalore Retailers Ltd.)
        buyer_user = User(
            email="procurement@ecofab.in",
            hashed_password=default_pw,
            full_name="Arvind Deshmukh",
            phone="+91 98200 44521",
            role="BUYER",
            is_active=True
        )
        db.add(buyer_user)
        db.flush()

        buyer_profile = Buyer(
            user_id=buyer_user.id,
            organization_name="EcoFab Bangalore Retailers Ltd.",
            gst_number="29AAACE1234F1Z8",
            contact_person="Arvind Deshmukh (Procurement Head)",
            address="Peenya Industrial Area, Bengaluru, Karnataka",
            verified=True
        )
        db.add(buyer_profile)

        # 4. Federation Officer: Deepa Narayan, KAS
        federation_officer = User(
            email="deepa.narayan@ksrlps.gov.in",
            hashed_password=default_pw,
            full_name="Deepa Narayan, KAS",
            phone="+91 94481 02941",
            role="FEDERATION_OFFICER",
            is_active=True
        )
        db.add(federation_officer)

        # 5. Customer: Pooja Hegde
        customer_user = User(
            email="pooja.h@gmail.com",
            hashed_password=default_pw,
            full_name="Pooja Hegde",
            phone="+91 99801 33490",
            role="CUSTOMER",
            is_active=True
        )
        db.add(customer_user)
        db.flush()

        print("Seeding SHG: Pragati Mahila Sangha...")
        shg = SHG(
            name="Pragati Mahila Sangha",
            registration_number="KA-RAM-NRLM-2022-044",
            address="Ramanagara Cluster, Channapatna Taluk",
            district="Ramanagara",
            state="Karnataka",
            bank_account_details="State Bank of India, Channapatna Branch, A/C: 38291048291, IFSC: SBIN0040192",
            leader_id=leader.id
        )
        db.add(shg)
        db.flush()

        # Seed SHG Members and MemberCapacities
        shg_members_list = []
        for u, skills, hrs, on_time, level, speed, workload, village, acct in shg_member_users:
            m = SHGMember(
                user_id=u.id,
                shg_id=shg.id,
                skills=json.dumps(skills),
                bank_account_number=acct,
                ifsc_code=acct.split(" ")[0] if " " in acct else "SBIN0040192",
                is_active=True
            )
            db.add(m)
            db.flush()
            shg_members_list.append((m, u, skills, hrs, on_time, level, speed, workload, village, acct))

            cap = MemberCapacity(
                member_id=m.id,
                product_specialization=skills[0],
                available_hours_per_day=hrs,
                current_workload=float(workload),
                max_feasible_daily_quantity=round(speed * hrs, 1),
                historical_completion_rate=on_time,
                active_tasks_count=1
            )
            db.add(cap)

        print("Seeding Products Catalog...")
        p_tote = Product(
            name="Organic Cotton Tote Bags (Heavy 280 GSM)",
            category="Garments & Textiles",
            description="100% natural unbleached cotton canvas tote bag, reinforced cross handles, inner zip pocket",
            base_unit="piece",
            standard_rate=165.0,
            is_active=True
        )
        p_runner = Product(
            name="Kasuti Embroidered Jute Table Runners",
            category="Handicrafts & Decor",
            description="Golden natural jute 350 GSM with traditional Ilkal Kasuti border thread work",
            base_unit="piece",
            standard_rate=380.0,
            is_active=True
        )
        p_turmeric = Product(
            name="Stone-Ground Curcumin Rich Turmeric 500g Jars",
            category="Food Products",
            description="Salem variety turmeric cold-milled in amber food-grade PET jars",
            base_unit="jar",
            standard_rate=195.0,
            is_active=True
        )
        db.add_all([p_tote, p_runner, p_turmeric])
        db.flush()

        print("Seeding Bulk Orders...")
        # Order 1: ORD-2026-104
        order104 = BulkOrder(
            order_number="ORD-2026-104",
            buyer_id=buyer_profile.id,
            shg_id=shg.id,
            title="Organic Cotton Tote Bags (Heavy 280 GSM)",
            description="1,200 heavy cotton canvas tote bags for retail grocery store chain",
            status=OrderStatus.IN_PRODUCTION.value,
            target_delivery_date=datetime.now(timezone.utc) + timedelta(days=13),
            total_order_value=198000.0,
            approved_price_per_unit=165.0,
            currency="INR",
            notes="100% natural unbleached cotton, double reinforced X-stitch cross handle, inner 6x6 zipper pocket."
        )
        # Order 2: ORD-2026-108
        order108 = BulkOrder(
            order_number="ORD-2026-108",
            buyer_id=buyer_profile.id,
            shg_id=shg.id,
            title="Kasuti Embroidered Jute Table Runners",
            description="500 table runners for festive exhibition",
            status=OrderStatus.IN_PRODUCTION.value,
            target_delivery_date=datetime.now(timezone.utc) + timedelta(days=23),
            total_order_value=190000.0,
            approved_price_per_unit=380.0,
            currency="INR",
            notes="Golden natural jute 350 GSM with traditional Ilkal Kasuti border thread work."
        )
        # Order 3: ORD-2026-112
        order112 = BulkOrder(
            order_number="ORD-2026-112",
            buyer_id=buyer_profile.id,
            shg_id=shg.id,
            title="Stone-Ground Curcumin Rich Turmeric 500g Jars",
            description="800 jars of certified organic Salem turmeric",
            status=OrderStatus.DRAFT.value,
            target_delivery_date=datetime.now(timezone.utc) + timedelta(days=28),
            total_order_value=156000.0,
            approved_price_per_unit=195.0,
            currency="INR",
            notes="Certified organic Salem variety turmeric, cold-milled, airtight amber PET jars."
        )
        db.add_all([order104, order108, order112])
        db.flush()

        item104 = OrderItem(
            bulk_order_id=order104.id,
            product_id=p_tote.id,
            quantity=1200,
            unit_price=165.0,
            completed_quantity=840,
            pending_quantity=360,
            specifications="100% natural unbleached cotton, double reinforced X-stitch cross handle, inner 6x6 zipper pocket."
        )
        item108 = OrderItem(
            bulk_order_id=order108.id,
            product_id=p_runner.id,
            quantity=500,
            unit_price=380.0,
            completed_quantity=120,
            pending_quantity=380,
            specifications="Golden natural jute 350 GSM, Ilkal Kasuti border work."
        )
        item112 = OrderItem(
            bulk_order_id=order112.id,
            product_id=p_turmeric.id,
            quantity=800,
            unit_price=195.0,
            completed_quantity=0,
            pending_quantity=800,
            specifications="Certified organic Salem variety turmeric, cold-milled, food-grade airtight amber PET jars."
        )
        db.add_all([item104, item108, item112])
        db.flush()

        print("Seeding Pricing Breakdown for ORD-2026-104...")
        pricing104 = PricingBreakdown(
            bulk_order_id=order104.id,
            total_material_cost=103680.0 + 13440.0 + 7800.0 + 5760.0,
            labor_cost=38400.0,
            packaging_cost=4200.0,
            transportation_cost=3840.0,
            operational_expenses=4800.0,
            profit_margin_percentage=8.12,
            calculated_unit_price=151.6,
            suggested_selling_price=165.0,
            final_approved_price=165.0,
            is_approved=True,
            approved_by_id=leader.id,
            approved_at=datetime.now(timezone.utc) - timedelta(days=20),
            notes="Costing model verified with 8.1% net SHG reserve profit."
        )
        db.add(pricing104)

        print("Seeding Work Allocations for ORD-2026-104...")
        allocations_data = [
            (shg_members_list[0][0], 220, 180, 32.0, "Main Body Stitching & Handle Assembly"),
            (shg_members_list[1][0], 220, 150, 32.0, "Heavy Canvas Fabric Cutting & Pattern Sizing"),
            (shg_members_list[2][0], 200, 140, 32.0, "Reinforced Cross-Stitching & Hemming"),
            (shg_members_list[3][0], 180, 120, 32.0, "Inner Zipper Pocket Sub-Assembly"),
            (shg_members_list[4][0], 180, 90, 32.0, "Screen Printing & Quality Finishing"),
            (shg_members_list[5][0], 160, 80, 32.0, "Steam Ironing, Thread Trimming & Tagging")
        ]

        work_allocs = []
        for mem, alloc_q, comp_q, rate, task in allocations_data:
            wa = WorkAllocation(
                bulk_order_id=order104.id,
                order_item_id=item104.id,
                member_id=mem.id,
                allocated_quantity=alloc_q,
                completed_quantity=comp_q,
                unit_rate=rate,
                status=AllocationStatus.IN_PROGRESS.value,
                deadline=datetime.now(timezone.utc) + timedelta(days=12),
                ai_recommended=True
            )
            db.add(wa)
            work_allocs.append(wa)
        db.flush()

        print("Seeding Batches & Quality Inspections...")
        batch1 = ProductionBatch(
            bulk_order_id=order104.id,
            work_allocation_id=work_allocs[0].id,
            batch_number="QCB-2026-081",
            quantity=50,
            status=BatchStatus.ACCEPTED.value,
            photo_urls=json.dumps(["https://images.unsplash.com/photo-1597484661643-2f5fef640dd1"])
        )
        batch2 = ProductionBatch(
            bulk_order_id=order104.id,
            work_allocation_id=work_allocs[3].id,
            batch_number="QCB-2026-085",
            quantity=35,
            status=BatchStatus.SUBMITTED.value,
            photo_urls=json.dumps(["https://images.unsplash.com/photo-1544816155-12df9643f363"])
        )
        db.add_all([batch1, batch2])
        db.flush()

        insp1 = QualityInspection(
            production_batch_id=batch1.id,
            status=QualityStatus.APPROVED.value,
            ai_score=94.2,
            ai_defects_detected=json.dumps([{"type": "Handle Cross Stitch", "severity": "LOW", "detail": "Minor tension variance; passes 15kg pull"}]),
            ai_explanation="Pass with minor warning. High strength seam verified.",
            ai_suggested_action="APPROVE_WITH_MINOR_REWORK",
            human_decision="APPROVED",
            human_reviewer_id=leader.id,
            reviewed_at=datetime.now(timezone.utc) - timedelta(days=2)
        )
        insp2 = QualityInspection(
            production_batch_id=batch2.id,
            status=QualityStatus.PENDING_HUMAN_REVIEW.value,
            ai_score=89.5,
            ai_defects_detected=json.dumps([{"type": "Zipper Alignment", "severity": "MEDIUM", "detail": "Wavy stitching along inner zipper on 6 units"}]),
            ai_explanation="Recommend rework on 6 units for zipper restitching prior to carton packing.",
            ai_suggested_action="REWORK_RECOMMENDED",
            human_decision=None,
            human_reviewer_id=None
        )
        db.add_all([insp1, insp2])

        print("Seeding Inventory & Suppliers...")
        inv_items = [
            ("Heavy 280 GSM Unbleached Cotton Canvas", InventoryItemType.RAW_MATERIAL.value, "Meters", 1850.0, 1440.0, 60.0, 72.0, 250.0),
            ("Natural Cotton Herringbone Webbing (38mm)", InventoryItemType.RAW_MATERIAL.value, "Meters", 2400.0, 1680.0, 80.0, 8.0, 300.0),
            ("Inner 6x6 Brass-Coil Zippers", InventoryItemType.RAW_MATERIAL.value, "Units", 1500.0, 1200.0, 50.0, 6.5, 200.0),
            ("Screen-Printing Eco Water-Based Black Pigment", InventoryItemType.RAW_MATERIAL.value, "Liters", 45.0, 30.0, 2.0, 380.0, 10.0),
            ("Certified Salem Variety Organic Raw Turmeric", InventoryItemType.RAW_MATERIAL.value, "Kilograms", 600.0, 400.0, 0.0, 120.0, 150.0),
            ("Golden Natural Jute Fabric 350 GSM", InventoryItemType.RAW_MATERIAL.value, "Meters", 750.0, 600.0, 20.0, 95.0, 100.0)
        ]
        for name, cat, unit, phys, bulk_res, ret_res, cost, low_th in inv_items:
            inv = Inventory(
                shg_id=shg.id,
                item_name=name,
                item_type=cat,
                unit=unit,
                physical_stock=phys,
                bulk_reserved_stock=bulk_res,
                retail_reserved_stock=ret_res,
                unit_cost=cost,
                low_stock_threshold=low_th
            )
            db.add(inv)

        sup1 = Supplier(name="Venkateshwara Weaving Mills", contact_person="R. Muralidharan", phone="+91 94480 33190", email="murali@venkateshwara.in", address="Davanagere Textile Hub", materials_supplied=json.dumps(["Heavy Cotton Canvas 280 GSM", "Grey Cloth 220 GSM"]), reliability_score=96.0)
        sup2 = Supplier(name="Sri Lakshmi Tapes & Ribbons", contact_person="K. Venkatesh", phone="+91 98860 12093", email="venkatesh@srilakshmi.in", address="Rajajinagar, Bangalore", materials_supplied=json.dumps(["Cotton Webbing Handles", "Jute Twine Ribbons"]), reliability_score=92.0)
        sup3 = Supplier(name="GreenEarth Packaging Solutions", contact_person="Ananya Hegde", phone="+91 99002 81123", email="ananya@greenearth.in", address="Bidadi Industrial Area", materials_supplied=json.dumps(["Recycled Kraft Cartons", "Eco Cotton Tags"]), reliability_score=98.0)
        db.add_all([sup1, sup2, sup3])

        print("Seeding Logistics & Shipments...")
        shipment1 = Shipment(
            bulk_order_id=order104.id,
            shipment_number="LOG-OUT-902",
            total_quantity=500,
            carrier_name="VRL Village Logistics & Rural Express",
            status="DISPATCHED",
            dispatch_date=datetime.now(timezone.utc) - timedelta(days=1),
            expected_delivery_date=datetime.now(timezone.utc) + timedelta(days=2),
            delivery_notes="Batch 1: 500 Completed Cotton Tote Bags (10 master cartons)"
        )
        db.add(shipment1)

        print("Seeding Earnings & Payout Workflow for ORD-2026-104...")
        earning_amounts = [5760.0, 4800.0, 4480.0, 3840.0, 2880.0, 2560.0]
        for i, (mem, alloc_q, comp_q, rate, task) in enumerate(allocations_data):
            e = MemberEarning(
                member_id=mem.id,
                bulk_order_id=order104.id,
                work_allocation_id=work_allocs[i].id,
                assigned_quantity=alloc_q,
                accepted_quantity=comp_q,
                approved_rate=rate,
                gross_earnings=earning_amounts[i],
                deductions=0.0,
                net_payable_amount=earning_amounts[i],
                payment_status=EarningPaymentStatus.CALCULATED.value
            )
            db.add(e)

        payout104 = Payout(
            shg_id=shg.id,
            payout_reference="PAY-ORD-2026-104-M1",
            period_start=datetime.now(timezone.utc) - timedelta(days=15),
            period_end=datetime.now(timezone.utc),
            total_amount=sum(earning_amounts),
            status=PayoutStatus.PENDING_GROUP_APPROVAL.value,
            notes="Interim Milestone 1 (600 Approved Bags) payout awaiting 60% member quorum."
        )
        db.add(payout104)

        print("Seeding AI Audit Records & Agent Activities...")
        ai_records = [
            ("ORDER_PLANNING", order104.id, "BulkOrder", {"order_id": order104.id, "quantity": 1200}, {"recommendation": "Dividing 1,200 units across 6 members with staggered 4-day milestones ensures on-time completion by Nov 18.", "confidence": 0.95}, 0.95, "SUCCESS"),
            ("WORK_ALLOCATION_LP", order104.id, "BulkOrder", {"order_id": order104.id}, {"recommendation": "Optimal LP distribution minimizes bottleneck risk with 100% capacity feasibility.", "confidence": 0.92}, 0.92, "SUCCESS"),
            ("CV_QUALITY_INSPECTION", batch2.id, "ProductionBatch", {"batch_id": batch2.id}, {"defect": "Zipper alignment divergence (>3mm)", "ai_action": "REWORK_RECOMMENDED"}, 0.895, "SUCCESS"),
            ("PRICING_INTELLIGENCE", order104.id, "BulkOrder", {"unit_price": 165.0}, {"margin": 8.12, "benchmark": "Bangalore wholesale rate 160-175 INR"}, 0.91, "SUCCESS")
        ]
        for cap_type, ref_id, ref_t, req_p, res_p, conf, st in ai_records:
            ar = AIAnalysisRecord(
                capability_type=cap_type,
                reference_id=ref_id,
                reference_type=ref_t,
                request_payload_json=json.dumps(req_p),
                response_payload_json=json.dumps(res_p),
                confidence_score=conf,
                status=st
            )
            db.add(ar)

        db.commit()
        print("\nPragati Mahila Sangha Demo Dataset Seeded Successfully!")
        print("----------------------------------------------------------------")
        print("1-Click Demo Accounts (All use password: Saathi@2026):")
        print("  SHG Leader:         savitribai@pragati-shg.org")
        print("  SHG Member:         sunita.rathod@shg.in")
        print("  Wholesale Buyer:    procurement@ecofab.in")
        print("  Federation Officer: deepa.narayan@ksrlps.gov.in")
        print("  Retail Customer:    pooja.h@gmail.com")
        print("----------------------------------------------------------------")

    except Exception as e:
        db.rollback()
        print(f"Error seeding demo data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_full_demo()
