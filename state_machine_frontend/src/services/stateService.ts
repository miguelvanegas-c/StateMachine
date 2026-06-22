const states = [
  { name: "PENDING", events: ["PENDINGBIOMETRICALVERIFICATION", "NOVERIFICATIONNEEDED", "PAYMENTFAILED", "ORDERCANCELLED", "ORDERCANCELLEDBYUSER"] },
  { name: "ONHOLD", events: ["BIOMETRICALVERIFICATIONSUCCESSFUL", "VERIFICATIONFAILED", "ORDERCANCELLEDBYUSER", "ORDERCANCELLEDBYUSER"] },
  { name: "PENDINGPAYMENT", events: ["PAYMENTSUCCESSFUL", "ORDERCANCELLEDBYUSER"] },
  { name: "CONFIRMED", events: ["PREPARINGSHIPMENT", "ORDERCANCELLEDBYUSER"] },
  { name: "PROCESSING", events: ["ITEMDISPATCHED", "ORDERCANCELLEDBYUSER"] },
  { name: "SHIPPED", events: ["ITEMRECEIVEDBYCUSTOMER", "DELIVERYISSUE", "ORDERCANCELLEDBYUSER"] },
  { name: "DELIVERED", events: [] },
  { name: "CANCELLED", events: [] },
]

export const stateService = {
  getState(name: string) {
    return states.find(state => state.name === name) ?? { name: "", events: [] };
  }
}